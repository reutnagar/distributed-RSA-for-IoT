from state import *
from global_data import state
from scipy.optimize import fsolve
from math import log
import random, math, string, time
import messages, crypt

KEY_SIZE = 16

# memory size
M = 512

# The number of the nodes in network.
n = 10000

# the sub pool size is limited by the memory
def calculate_sub_keys_size():
	sub_pool = M/(2*KEY_SIZE)
	return sub_pool

# size of sub keys 
k = calculate_sub_keys_size()

# n', The neighborhood size
nn = 25

# a real constant, to calculate p is the probability that the two nodes are connected directly
c = 11.5
# calculate p, according to the variables. p is 
p = math.log(n, math.e)/n + c/n

# d is the expected value of the node
d = p * (n - 1)

# p' is the probability that two nodedes have a common-key
pp = d / (nn - 1)

# x0, the first x, in order to begins the iterations of calculating p'
gP = -k**2/math.log(1-pp)

# function to calculate p'.
def func(P):
	return log(1-pp)-(2*P-2*k+1)*log(1-k/P)+(P-2*k+1/2)*log(1-2*k/P) 
	
# function to calculate the size of the pool the master have to generate
def calculate_pool_size():
	P = int(fsolve(func, gP)[0])
	return P
	
# the size of the pool
P = calculate_pool_size()

#for the pool_testing
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
def nodesInNetwork():
	return n
	
# function to generate the pool
def generate_key_pool():
	key_pool = []  # list of keys
	for i in xrange(P):
		# generate a random sequence of bits to be the key
		key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
		key_pool.append(key)  # add the key to the pool. the key index is its index on this list
	print("Generated the key pool.")
	return key_pool

# needed to the pool_test
def generate_sub_keys(key_pool, k):
    sub_keys = {}
    for i in xrange(k):
        id = -1
        while id < 0 or id in sub_keys:
            id = int(math.floor(random.random() * len(key_pool)))
        sub_keys[id] = key_pool[id]
    return sub_keys

# function that sendings keys to clients that waiting for them
def send_keys():
	current_clients = state.toSendKeys
	state.toSendKeys = [] # reset the list of client that are waiting to receive the keys. this list may be changed from the async thread
	for index, client in enumerate(current_clients): # send the key to nodes that already sent their public key
		ip = client[index]
		messages.send_keys_to_client(ip, None)

