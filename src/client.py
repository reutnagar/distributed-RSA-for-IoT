import threading
import time
import socket
import os


STATE_MASTER = 0
STATE_ERROR = -1
STATE_TMP_CLIENT = 1
STATE_CLIENT = 2

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

class Client():
	
	def __init__(self):
		self.state = STATE_CLIENT
		self.strengh = 6	# self.calc_strengh()

	def calc_strengh(self):
		pass

	def broadcast(self):
		my_bc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_bc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		while self.state is not STATE_MASTER:
			time.sleep(2)
			my_bc_socket.sendto("I Am Master", ('<broadcast>' ,8881))
			print("sent message: I Am Master")
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

	def listen(self):
		my_lsn_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if os.name != "nt":	# for Arduino
			my_ip = get_interface_ip("apcli0")
		else: 				# for Windows PC
			my_ip = socket.gethostbyname(socket.gethostname())
		my_lsn_socket.bind(('',8881))
		message , address = my_lsn_socket.recvfrom(1024)
		if(my_ip != address[0]): # Each device gets its own msg, because it is broadcast
			print 'Got message: %s. from : %s' % ( str(message), address[0])
		return str(message)

	def process_message(self, msg):
		pass

	def run(self,REQUIRED_STRENGH):		
		if(self.strengh > REQUIRED_STRENGH):
			self.state = STATE_TMP_CLIENT
			self.async_action(self.broadcast)
		while((self.state is not STATE_MASTER) and (self.state is not STATE_ERROR)):
			msg = self.listen()
			self.process_message(msg)
		if(self.state == STATE_MASTER):
			return True
		return False