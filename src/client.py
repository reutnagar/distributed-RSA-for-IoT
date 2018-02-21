import threading
import time
import socket
import os
from global_defs import *
import internal_state



if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

class Client():
	
	def __init__(self):
		self.data = None
		self.sending_ip = ''
		self.sending_msg = ''
		self.msg_dict = {MSG_I_MASTER: self.proc_MSG_I_MASTER, MSG_YOU_MASTER: self.proc_MSG_YOU_MASTER, MSG_OK_I_MASTER: self.proc_MSG_OK_I_MASTER,}
    	
	def calc_strengh(self):
		return 10  # missing impl. for now

	def broadcast(self):
		my_bc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_bc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		while(True):
			time.sleep(2)
			if(self.data.state != STATE_TMP_CLIENT):
				my_bc_socket.close()
				return
			my_bc_socket.sendto(MSG_I_MASTER, ('<broadcast>' ,8881))
			print 'Sent broadcast message: %s' % MSG_I_MASTER
		my_bc_socket.close()
		return			

	def async_action(self, func_to_run):
		comm = threading.Thread(target=func_to_run)
		comm.daemon = True 	# the thread will be killed when main program exits
		comm.start()

	def getips(self, hostname):
	    try:
	        result = socket.getaddrinfo(hostname, None, socket.AF_INET,\
	            socket.SOCK_DGRAM, socket.IPPROTO_IP, socket.AI_CANONNAME)
	        list = result #[x[4][0] for x in result]
	        return list
	    except Exception, err:
	        print "error"
	    return ""

	def send_message(self,msg,ip):
		my_send_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_send_soc.sendto(msg,(ip ,8881))
		my_send_soc.close()
		print 'Sent message: %s, to: %s' % (str(msg),ip)

	def listen(self):
		my_lsn_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_lsn_socket.bind(('',8881))
		message , address = my_lsn_socket.recvfrom(1024)
		if(self.data.my_ip != address[0]): # Each device gets its own msg, because it is broadcast
			print 'Got message: %s. from : %s' % ( str(message), address[0])
		return str(message), address[0]
		
	def proc_MSG_I_MASTER(self):
		ip = self.sending_ip
        if(self.data.master_ip != ""): # already has a master
            return
        print 'in proc_MSG_I_MASTER'
        self.data.state = STATE_CLIENT
        self.data.master_ip = ip
        self.send_message(MSG_YOU_MASTER, ip)
		
	def proc_MSG_YOU_MASTER(self):
		ip = self.sending_ip
		print 'in proc_MSG_YOU_MASTER'
        if((self.data.state != STATE_TMP_CLIENT) or (self.data.master_ip != "")):
			return
		self.data.neighbors.append(ip)
		self.send_message(MSG_OK_I_MASTER, ip)
		
	def proc_MSG_OK_I_MASTER(self):
        ip = self.sending_ip
		print 'in proc_MSG_OK_I_MASTER'
		if(self.data.master_ip != ip):
			print 'Error! got MSG_OK_I_MASTER from new ip!'
			self.data.state = STATE_ERROR  # this will re-create the device as client
		#self.data.master_ip = ip
		print 'Setting: %s as my Master...' % (str(ip))

    def proc_MSG_UNDEFINED(self):
		ip = self.sending_ip
		msg = self.sending_msg
		print 'Undefined message: %s. from: %s. Ignore...' % (msg, str(ip))

    def process_message(self, msg, ip):
		if(ip == self.data.my_ip):
			return
		self.sending_ip = ip
		self.sending_msg = msg
		print 'in process_message. msg: %s' % msg
		return self.msg_dict.get(msg, self.proc_MSG_UNDEFINED)()

	def run(self,REQUIRED_STRENGH, my_state):
		print 'Client.run() is started...'
		# init internal data
		self.data = my_state
		self.data.state = STATE_CLIENT
		self.data.strengh = self.calc_strengh()
		if os.name != "nt":	# for Arduino
			self.data.my_ip = get_interface_ip("apcli0")
		else: 				# for Windows PC
			self.data.my_ip = socket.gethostbyname(socket.gethostname())
		# broadcast if needed
		if(self.data.strengh > REQUIRED_STRENGH):
			self.data.state = STATE_TMP_CLIENT
			self.async_action(self.broadcast)
		# listen & process messages
		while((self.data.state != STATE_MASTER) and (self.data.state != STATE_ERROR)):
			msg, ip = self.listen()
			self.process_message(msg, ip)
			if(self.data.state == STATE_MASTER):
				print 'my state == STATE_MASTER. returning to main...'
		return self.data