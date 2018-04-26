import struct
import threading
import socket
import time
import os

PORT = 8881
stateInt = None

if os.name != "nt":
    import fcntl
    #import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

if os.name != "nt": # for Arduino
    my_ip = get_interface_ip("apcli0")
else:               # for Windows PC
    my_ip = socket.gethostbyname(socket.gethostname())

print("My IP is: " + my_ip)

#############################
#### Async thread  ##########
#############################
def async_listenToMessages(state):
	global stateInt
	print("Creating New thread..")
	stateInt = state
	c = threading.Thread(target=asyncListen)  #, args=(9999,)
	c.daemon = True
	c.start()

def listen(socket):
	message , address = socket.recvfrom(1024)
	if(my_ip != address[0]): # Each device gets its own msg, because it is broadcast
		print 'Got message: %s. from : %s' % ( str(message), address[0])
	return str(message), address[0]


def asyncListen():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',PORT))
	while(True):  # may stop the thread on some condition...
		msg, ip = listen(s)  # block until message accepted
		process_message(message, ip)

def process_message(message, ip):
	if message == 'IS_THERE_MASTER' and state.status == 'MASTER_INIT or MASTER_DONE':
		print 'send message I_AM_MASTER to ip'
	else:
		if message == 'I_AM_MASTER' and state.status == 'NODE_INIT':
			state.status == 'MASTER_FOUND'
			state.masterIP = ip
		else: 
			if message == 'I_AM_ON_THE_NETWORK' and ip not in status.neighbors:
				status.neighbors.append(ip)
			else:
				if message == 'CLIENT_SUBSET_KEYS' and state.status == 'CLIENT_INIT':
					print 'recieve the list of the keys'


#############################
#### External API ###########
#############################

def _get_block(s, count):
    if count <= 0:
        return ''
    buf = ''
    while len(buf) < count:
        buf2 = s.recv(count - len(buf))
        if not buf2:
            # error or just end of connection?
            if buf:
                raise RuntimeError("underflow")
            else:
                return ''
        buf += buf2
    return buf

def _send_block(s, data):
    while data:
        data = data[s.send(data):]

def get_msg(s):
    count = struct.unpack('>i', _get_block(s, 4))[0]
    return _get_block(s, count)

def send_msg(s, data):
    header = struct.pack('>i', len(data))
    _send_block(s, header)
    _send_block(s, data)
    print '1'+header
    print '2'+data

def broadcast(message): #send broadcast message
	my_bc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	my_bc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)		
	my_bc_socket.sendto(message, ('<broadcast>' ,8881))
	print 'Sent broadcast message: %s' % message
	my_bc_socket.close()
	return

def send_single_msg(message,ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	c, addr = s.accept()
	send_msg(c, message)
	c.close()
	s.close()
	
	
	
	