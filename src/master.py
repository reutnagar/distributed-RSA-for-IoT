import threading
import time
import socket
import os
from global_defs import *
import internal_state


class Master():
    def __init__(self):
    	self.data = None
    	self.sending_ip = ''
    	self.sending_msg = ''
    	self.msg_dict = { MSG_YOU_MASTER: self.proc_MSG_YOU_MASTER,}

    def broadcast(self):
		my_bc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_bc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)		
		while(True):
			time.sleep(0.5) # no need any sleep, avoid busy loop
			if(self.data.net_state != NET_STATE_INIT):
				print 'Finished init of network. now processing data...'
				my_bc_socket.close()
				return
			my_bc_socket.sendto(MSG_I_MASTER, ('<broadcast>' ,8881))
			print 'Sent broadcast message: %s' % MSG_I_MASTER
		my_bc_socket.close()
		return

    def async_action(self, func_to_run):
        comm = threading.Thread(target=func_to_run)
        comm.daemon = True # the thread will be killed when main program exits
        comm.start()

    def send_message(self,msg,ip):
		my_send_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_send_soc.sendto(msg,(ip ,8881))
		my_send_soc.close()
		print 'Sent message: %s, to: %s' % (str(msg),ip)

    def listen(self, sock):
        message , address = sock.recvfrom(1024)
        if(self.data.my_ip != address[0]): # Each device gets its own msg, because it is broadcast
			print 'Got message: %s. from : %s' % ( str(message), address[0])
        return str(message), address[0]

    def proc_MSG_YOU_MASTER(self):
		ip = self.sending_ip
		print 'in proc_MSG_YOU_MASTER'
		self.data.neighbors.append(ip)  # add the ip of the node to internal list. will send to all clients later		pass
		self.send_message(MSG_OK_I_MASTER, ip)

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

    def establish_network(self, sec):
		start_time = time.time()  # returns time in seconds
		# broadcast in different thread
		self.async_action(self.broadcast)
		my_lsn_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_lsn_socket.bind(('',8881))
		while(time.time() < start_time + sec): # listen for 'sec' period
			msg, ip = self.listen(my_lsn_socket)
			self.process_message(msg, ip)
		my_lsn_socket.close()
		self.data.net_state = NET_STATE_KEY_CREATE # will kill broadcast thread
    
    def run(self, my_state):
    	print 'Master.run() is started...'
    	# init internal data
    	self.data = my_state
    	self.data.state = STATE_MASTER
    	self.data.net_state = NET_STATE_INIT
    	# establish another connections for a period of time
        self.establish_network(SEC_TO_INIT_NETWORK)
        # listen & process messages
    	# while(True): # should never return
    	# 	pass
    	return self.data