import struct, threading, pickle, socket, time, os
from state import *
from global_data import state
import crypt

IS_THERE_MASTER = "IS_THERE_MASTER"
I_AM_MASTER = "I_AM_MASTER"
CLIENT_PUBLIC_KEY = "CLIENT_PUBLIC_KEY"
CLIENT_RING_KEYS  = "CLIENT_RING_KEYS"
CLIENT_RING_END = "CLIENT_RING_END"
I_AM_ON_THE_NETWORK = "I_AM_ON_THE_NETWORK"
CLIENT_START_SESSION = "CLIENT_START_SESSION"
CLIENT_COMMON_INDEX  = "CLIENT_COMMON_INDEX"
MESSAGE_ENC_DATA = "MESSAGE_ENC_DATA"
PORT = 5002

# the messages have three fields: 
# 1. type = the header of the message
# 2. dataID = an aditional data, like the index of key in CLIENT_RING_KEYS message , when no nedded is 0
# 3. data = the data itself. when the message don't have data, it'w None 
class Message(object):
	def __init__(self, type, dataID, data):
		self.type = type
		self.dataID = dataID
		self.data = data

if os.name != "nt":
    import fcntl

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

# Our code supports several operating systems
if os.name == "nt": # for Windows PC
    my_ip = socket.gethostbyname(socket.gethostname())
elif os.name == "posix": # for Raspberry Pi
	my_ip = get_interface_ip("wlan0") # or "eth0" if using Ethernet
else: # for Arduino
    my_ip = get_interface_ip("apcli0")
               
state.myIP = my_ip
print("My IP is: " + my_ip)

#############################
#### Async thread  ##########
#############################
# async thread for listening, killed where no needed
def async_listen_to_messages():
	print("Creating New thread..")
	c = threading.Thread(target=async_listen)
	c.daemon = True
	c.start()

def async_listen():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',PORT))
	print("Created socket. Listening for messages...")
	while(True):  # may stop the thread on some condition...
		msg, ip = listen(s)  # block until message accepted
		process_message(msg, ip)

		
# listen for message, if it is not sent by me - process the message
def listen(socket):
	while True:
		bits , address = get_msg(socket)
		if my_ip != address[0]:
			break
	msg = pickle.loads(bits) # Returns the message to a format of Message class
	return msg, address[0]

# function to process the message, in order to know what to do with
def process_message(message, ip):
	print("Got message from " + str(ip) + ". Type: " + str(message.type) + ", dataID: " + str(message.dataID))
	if message.type == IS_THERE_MASTER:
		if (state.status == MASTER_INIT or state.status == MASTER_DONE): # if I'm master
			send_single_msg(ip,I_AM_MASTER) 
			print("Sent message I_AM_MASTER to IP: "+ str(ip))
	elif message.type == I_AM_MASTER: # if get I_AM_MASTER msg, set the sender IP to be a master
		if state.status == NODE_INIT:
			state.status = MASTER_FOUND
			state.masterIP = ip
			state.neighbors.append((ip,-1))
		elif state.status == INIT:
			print("Got message: I_AM_MASTER in INIT stage. doing nothing...")
	elif message.type == CLIENT_PUBLIC_KEY: # only the master can get this msg
		if state.status == MASTER_INIT:
			state.toSendKeys.append((ip,message.data)) # save the client ip and public key for later use
		elif state.status == MASTER_DONE:
			# encrypt the sub-pool with the client's public key
			c = threading.Thread(target=send_keys_to_client, args=[ip, message.data])
			c.daemon = True
			c.start()
	elif message.type == CLIENT_RING_KEYS:
		if state.status == CLIENT_INIT or state.status == CLIENT_GETTING_KEYS:
			print("Receive key, index: " + str(message.dataID))
			state.keys.append((message.dataID,message.data))
			state.status = CLIENT_GETTING_KEYS
	elif message.type == CLIENT_RING_END: # msg that say, finished to send keys
		if state.status == CLIENT_GETTING_KEYS:
			state.status = CLIENT_GOT_KEYS
	elif message.type == I_AM_ON_THE_NETWORK: # add the node to my neighbors
		ips = [i[0] for i in state.neighbors]
		if ip not in ips:
			print("Add neighbor ip: "+str(ip))
			state.neighbors.append((ip,-1))
			#print("the state.neighbors: "+str(state.neighbors))
		if(state.status == CLIENT_DONE or state.status == MASTER_DONE): # in this states can send the indexes to start talk
			my_indexes = [x[0] for x in state.keys]
			print("Sending my keys indexes to: "+str(ip))
			#print("My indexes are: "+str(my_indexes))
			send_single_msg(ip, CLIENT_START_SESSION,0,my_indexes)# send message to start talk
	elif message.type == CLIENT_START_SESSION: # check if have a common key with the sender
		ips = [i[0] for i in state.neighbors]
		if ip not in ips:
			print("Add neighbor ip: "+str(ip))
			state.neighbors.append((ip,-1))
		if state.status == CLIENT_DONE or state.status == MASTER_DONE:
			common_key = -1 
			# Intersect my keys & the sender keys
			common_keys = list(set(message.data).intersection([x[0] for x in state.keys]))
			# If common key is found- update internal state
			if common_keys: 
				for index, neighbor in enumerate(state.neighbors):
					list_neighbor = list(neighbor)
					if list_neighbor[0] == ip:
						list_neighbor[1]= common_keys[0]
					state.neighbors[index] = tuple(list_neighbor)
				common_key = common_keys[0]
			# Response with the common key index, or -1 if not found
			send_single_msg(ip, CLIENT_COMMON_INDEX,common_key)
			print("Common key with "+ str(ip) +" is: "+str(common_key))
	elif message.type == CLIENT_COMMON_INDEX:# receive the common index,and save it
		print("Common key with "+ str(ip) +" is: "+str(message.dataID))
		for index, neighbor in enumerate(state.neighbors):
			list_neighbor = list(neighbor)
			#print("list_neighbor: "+str(list_neighbor)) 
			if list_neighbor[0] == ip:
				list_neighbor[1] = message.dataID
			state.neighbors[index] = tuple(list_neighbor)
			#print('neighbors: '+str(state.neighbors))
	elif message.type == MESSAGE_ENC_DATA: # recieving data encypted with the common key
		for neighbor, index in state.neighbors: # look for the sender ip in the neighbors list
			if neighbor == ip: # neighbor is found
				# supposed to find only one key with the same index!
				key = ''.join([key for (i, key) in state.keys if i == index]) 
				msg = crypt.decrypt_message(key, message.data, message.dataID)
				print("Decrypted message from: "+ str(ip) + ". Message is: " + str(msg))
	else: #error
		print("Got message: "+ str(message.type)+ " when status is: "+ str(state.status))


#############################
#### External API ###########
#############################

# get block of msg
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

# send block of msg 
def _send_block(s, data, ip):
	while data:
		data = data[s.sendto(data, (ip,PORT)):]

# get all the message
def get_msg(s):
	header, ip = _get_block(s, 4)
	count = struct.unpack('>i', header)[0]
	return _get_block(s, count)

# send all the message
def send_msg(s, data, ip):
	header = struct.pack('>i', len(data))
	_send_block(s, header, ip)
	_send_block(s, data, ip)

def broadcast(type, dataID=0, data=None): #send broadcast message
	send_single_msg('<broadcast>', type, dataID, data)

def send_single_msg(ip, type, dataID=0, data=None):
	print("Sending message " +str(type)+" to: "+ str(ip))
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	if ip == '<broadcast>':
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	# serialize the message to a byte stream
	msg = Message(type,dataID,data)
	bits = pickle.dumps(msg) # format the msg
	send_msg(s, bits, ip)
	s.close()

# function that sending keys to clients that waiting for them, encrypted with their public key
# this will happen asynchronously
def send_keys_to_client(ip, clientPublicKey):
	print("Sending keys to: " + str(ip) + "...")
	# Send sub-pool of size determined in calculate_sub_keys_size()
	for i in range(state.subKeysSize): 
		# Get random key from the pool
		key_index = int(math.floor(random.random() * len(state.pool_keys)))
		keyData = state.pool_keys[key_index]
		# Encrypt the key with the client's public RSA key
		keyData = crypt.encrypt_asym(clientPublicKey, keyData)
		# Send to client
		send_single_msg(ip, 'CLIENT_RING_KEYS', key_index, keyData)
	# Indicate the client that no more keys will be sent
	send_single_msg(ip, 'CLIENT_RING_END')
	print("Finish to send keys to client.")


global openedSocket
global openedSocketSize

# because it a msg with a variable size
# we count the msg and send the header that contains the size of the msg
# and after it send blocks of messages.
# when recieved in blocks all the msg (by the header) - we know the next block us for the next msg

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

	
	
