from state import *
from global_data import state
from scipy.optimize import fsolve
from math import log
import random, math, string, time
import messages, crypt

KEY_SIZE = 16
# memory size
M = 512

# The number of network&#39;s nodes
n = 10000

def nodesInNetwork():
	return n

def calculate_sub_keys_size():
	print("Master: Calculating  the subset size = " + str(M/KEY_SIZE))
	return 15 #30 #15 #M/8
	
# size of sub keys 
k = calculate_sub_keys_size()

# n', neighborhood size
nn = 25

# # the probability where it is certainly true that two nodes have a connectivity
# Pc = 0.999

# def calculateC(Pc):
	# a = math.log(Pc,math.e)
	# b = -math.log(a,math.e)
	# return b

# c = calculateC(Pc)

c = 11.5

def a():
	Pc = math.e**(math.e**-c)
	return Pc
	
p = math.log(n, math.e)/n + c/n

d = p * (n - 1)

pp = d / (nn - 1) # p'

gP = -k**2/math.log(1-pp) #x0

# function to calculate p'
def func(P):
    return log(1-pp)-(2*P-2*k+1)*log(1-k/P)+(P-2*k+1/2)*log(1-2*k/P) 
	
def calculate_pool_size():
	print("Master: Calculating  the pool size...")
	P = int(fsolve(func, gP)[0])
	return P
	
# the size of the pool
P = calculate_pool_size()

def get_pp():
	return pp
	
def get_P():
	return P

def get_nn():
	return nn

def get_n():
	return n
	
def get_k():
	return k
	
def generate_key_pool():
	print("Master: Generating the key pool")
	key_pool = []  # list of keys
	for i in xrange(P):
		# generate a random sequence of bits to be the key
		key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
		key_pool.append(key)  # add the key to the pool. the key index is its index on this list
	print("Generated pool of size: "+ str(len(key_pool)))
	print(key_pool)
	return key_pool
	
def generate_sub_keys(key_pool, k):
    sub_keys = {}
    for i in xrange(k):
        id = -1
        while id < 0 or id in sub_keys:
            id = int(math.floor(random.random() * len(key_pool)))
        sub_keys[id] = key_pool[id]
    return sub_keys
	
def send_keys():
	print('in send_keys')
	current_clients = state.toSendKeys
	state.toSendKeys = [] # reset the list of client that are waiting to receive the keys. this list may be changed from the async thread
	for index, client in enumerate(current_clients): # send the key to nodes that already sent their public key
		ip = client[index]
		send_keys_to_client(ip, None)

def send_keys_to_client(ip, clientPublicKey):
	# Send sub-pool of size determined in calculate_sub_keys_size()
	for i in range(state.subKeysSize): 
		# Get random key from the pool
		key_index = int(math.floor(random.random() * len(state.pool_keys)))
		keyData = state.pool_keys[key_index]
		# Encrypt the key with the client's public RSA key
		keyData = crypt.encrypt_asym(clientPublicKey, keyData)
		# Send to client
		messages.send_single_msg(ip, 'CLIENT_RING_KEYS', key_index, keyData)
	# Indicate the client that no more keys will be sent
	messages.send_single_msg(ip, 'CLIENT_RING_END')
	
	
