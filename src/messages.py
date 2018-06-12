import struct, threading, pickle, socket, time, os
from state import *
from global_data import state

IS_THERE_MASTER = "IS_THERE_MASTER"
I_AM_MASTER = "I_AM_MASTER"
CLIENT_PUBLIC_KEY = "CLIENT_PUBLIC_KEY"
CLIENT_RING_KEYS  = "CLIENT_RING_KEYS"
CLIENT_RING_END = "CLIENT_RING_END"
I_AM_ON_THE_NETWORK = "I_AM_ON_THE_NETWORK"
CLIENT_START_SESSION = "CLIENT_START_SESSION"
CLIENT_COMMON_INDEX  = "CLIENT_COMMON_INDEX"
PORT = 5001

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

if os.name == "nt": # for Windows PC
    my_ip = socket.gethostbyname(socket.gethostname())
elif os.name == "posix": # for Ubuntu
	my_ip = get_interface_ip("eth0")
else: # for Arduino
    my_ip = get_interface_ip("apcli0")
               

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
		bits , address = get_msg(socket)
		if my_ip != address[0]:
			break
	msg = pickle.loads(bits)
	print('Got message: %s. from : %s' % (msg.type, address[0]))
	return msg, address[0]


def process_message(message, ip):
	print("in process_message. msg: "+ str(message.type))
	if message.type == IS_THERE_MASTER:
		if (state.status == MASTER_INIT or state.status == MASTER_DONE):
			send_single_msg(I_AM_MASTER,0,None, ip)
			#state.toSendKeys.append(ip) # TODO: if MASTER_DONE- send now
			#print state.toSendKeys
			print("Sent message I_AM_MASTER to IP: "+ str(ip))
	elif message.type == I_AM_MASTER:
		if state.status == NODE_INIT:
			state.status = MASTER_FOUND
			state.masterIP = ip
			state.neighbors.append((ip,-1))
			print("in process_message I_AM_MASTER. Master is found!! master IP is : "+ str(ip))
		elif state.status == INIT:
			print("Got message: I_AM_MASTER in INIT stage. doing nothing...")
		else:
			print("ERROR! got message: "+ str(message)+ "when status is: "+ str(state.status))
	elif message.type == CLIENT_PUBLIC_KEY: 
		if (state.status == MASTER_INIT or state.status == MASTER_DONE):
			# ips = [i[0] for i in state.neighbors]
			# if ip not in ips:
				# state.neighbors.append((ip,-1))
			state.toSendKeys.append((ip,-1)) # TODO: if MASTER_DONE- send now
			print(state.toSendKeys)
	elif message.type == CLIENT_RING_KEYS:
		if state.status == CLIENT_INIT or state.status == CLIENT_GETTING_KEYS:
			print("Receive key, index: "+str(message.dataID))
			state.keys.append((message.dataID,message.data))
			state.status = CLIENT_GETTING_KEYS
	elif message.type == CLIENT_RING_END:
		if state.status == CLIENT_GETTING_KEYS:
			print('Finish to recieve the keys')
			state.status = CLIENT_GOT_KEYS
			print('keys: '+str(state.keys))
	elif message.type == I_AM_ON_THE_NETWORK:
		ips = [i[0] for i in state.neighbors]
		if ip not in ips:
			print("Add neighbor ip: "+str(ip))
			state.neighbors.append((ip,-1))
			print("the state.neighbors: "+str(state.neighbors))
	elif message.type == CLIENT_START_SESSION:
		if state.status == CLIENT_DONE or state.status == MASTER_DONE:
			data_id = -1
			print('message.data: '+str(message.data))
			common_keys = list(set(message.data).intersection([x[0] for x in state.keys]))
			print('common keys: '+str(common_keys))
			if common_keys: 
				for index, neighbor in enumerate(state.neighbors):
					list_neighbor = list(neighbor)
					print("list_neighbor: "+str(list_neighbor)) 
					if list_neighbor[0] == ip:
						list_neighbor[1]= common_keys[0]
					state.neighbors[index] = tuple(list_neighbor)
					print('neighbors: '+str(state.neighbors))
				data_id = common_keys[0]
			#messages.send_single_msg(CLIENT_COMMON_INDEX,-1,None,ip)
			broadcast(CLIENT_COMMON_INDEX,data_id,None)
	elif message.type == CLIENT_COMMON_INDEX:
		print('got CLIENT_COMMON_INDEX msg, the common_key is: '+str(message.dataID))
		for index, neighbor in enumerate(state.neighbors):
			list_neighbor = list(neighbor)
			print("list_neighbor: "+str(list_neighbor)) 
			if list_neighbor[0] == ip:
				list_neighbor[1] = message.dataID
			state.neighbors[index] = tuple(list_neighbor)
			print('neighbors: '+str(state.neighbors))
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
	print("in send_msg. count is: "+ str(len(data)))
	_send_block(s, header, ip)
	_send_block(s, data, ip)

def broadcast(type, dataID, data): #send broadcast message
	print("Broadcast massage: "+ str(type))
	send_single_msg(type, dataID, data, '<broadcast>')

def send_single_msg(type, dataID, data,ip):
	print("in send_single_msg. sending message " +str(type)+" to: "+ str(ip))
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	if ip == '<broadcast>':
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	# serialize the message to a byte stream
	msg = Message(type,dataID,data)
	bits = pickle.dumps(msg)
	send_msg(s, bits, ip)
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

	
	