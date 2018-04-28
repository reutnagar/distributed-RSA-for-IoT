import struct
import threading
import socket
import time
import os
from state import *
from global_data import state

IS_THERE_MASTER = "IS_THERE_MASTER"
I_AM_MASTER = "I_AM_MASTER"
CLIENT_KEYS = "CLIENT_KEYS"
PORT = 8882


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
def async_listen_to_messages():
	print("Creating New thread..")
	c = threading.Thread(target=async_listen)
	c.daemon = True
	c.start()

def async_listen():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',PORT))
	print("Created socket...")
	while(True):  # may stop the thread on some condition...
		msg, ip = listen(s)  # block until message accepted
		process_message(msg, ip)

def listen(socket):
	while True:
	  message , address = get_msg(socket)
	  if my_ip != address[0]:
		break
	print 'Got message: %s. from : %s' % (str(message), address[0])
	return str(message), address[0]


def process_message(message, ip):
	print("in process_message. msg: "+ str(message))
	if message == 'IS_THERE_MASTER':
		if (state.status == MASTER_INIT or state.status == MASTER_DONE):
			send_single_msg(I_AM_MASTER, ip)
			state.toSendKeys.append(ip) # TODO: if MASTER_DONE- send now
			print("Sent message I_AM_MASTER to IP: "+ str(ip))
	elif message == 'I_AM_MASTER':
		if state.status == NODE_INIT:
			state.status = MASTER_FOUND
			state.masterIP = ip
			print("in process_message I_AM_MASTER. Master is found!!")
		elif state.status == INIT:
			print("Got message: I_AM_MASTER in INIT stage. doing nothing...")
		else:
			print("ERROR! got message: "+ str(message)+ "when status is: "+ str(state.status))
	elif message == 'I_AM_ON_THE_NETWORK': 
		if ip not in status.neighbors:
			status.neighbors.append(ip)
	elif message == 'CLIENT_SUBSET_KEYS':
		if state.status == 'CLIENT_INIT':
			print 'recieve the list of the keys'
	else:
		print("ERROR! got message: "+ str(message)+ "when status is: "+ str(state.status))


#############################
#### External API ###########
#############################

def _get_block(s, count):
    if count <= 0:
        return ''
    buf = ''
    while len(buf) < count:
        buf2, address = s.recvfrom(count - len(buf))
        if not buf2:
            # error or just end of connection?
            if buf:
                raise RuntimeError("underflow")
            else:
                return ''
        buf += buf2
    return buf, address

def _send_block(s, data, ip):
    while data:
        data = data[s.sendto(data, (ip,PORT)):]

def get_msg(s):
	header, ip = _get_block(s, 4)
	count = struct.unpack('>i', header)[0]
	print("in get_msg. count is: "+ str(count))
	return _get_block(s, count)

def send_msg(s, data, ip):
	header = struct.pack('>i', len(data))
	_send_block(s, header, ip)
	_send_block(s, data, ip)
	print '1'+header
	print '2'+data

def broadcast(message): #send broadcast message
	print("Broadcast massage: "+ message)
	send_single_msg(message, '<broadcast>')

def send_single_msg(message,ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	if ip == '<broadcast>':
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	send_msg(s, message, ip)
	s.close()


global openedSocket
global openedSocketSize

def send_header(size,ip):
	global openedSocket
	global openedSocketSize
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	header = struct.pack('>i', size)
	_send_block(s, header, ip)
	openedSocket = s
	openedSocketSize = size

def send_data(data,ip):
	global openedSocket
	global openedSocketSize
	_send_block(openedSocket, data, ip)
	openedSocketSize -= len(data)
	if(openedSocketSize <= 0):
		openedSocket.close()


# def send_multiple_msg(size,data,ip):
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	s.connect(('', PORT))
# 	send_header(size,ip)
# 	send_data(s, data)
# 	print(header)
# 	print(data)
	
	
	