from state import *
from global_data import state
from scipy.optimize import fsolve
from math import log
import random, math, string, time
import messages

KEY_SIZE = 20
# memory size
M = 512
# The number of network&#39;s nodes
n = 100
# the probability where it is certainly true that two nodes have a connectivity
Pc = 0.9

def calculate_sub_keys_size():
	print("Master: Calculating  the subset size = " + str(M/8))
	return M/8
	
# size of sub keys 
k = calculate_sub_keys_size()

# n' neighborhood size
nn = 30
c = 50 # ?? real constant
p = math.log(n, math.e)/n - c/n
d = p * (n - 1)
pp = d / (nn - 1) # p'
gP = -k**2/math.log(1-pp)

# function to calculate p'
def func(P):
    return log(1-pp)-(2*P-2*k+1)*log(1-k/P)+(2*P-4*k+1)*log(1-2*k/P) 
	
def calculate_pool_size():
	print("Master: Calculating  the pool size...")
	P = int(fsolve(func, gP)[0])
	return P
	
# the size of the pool
P = calculate_pool_size()
	
def generate_key_pool():
	print("Master: Generating the key pool")
	key_pool = []  # list of keys
	for i in xrange(P):
		# generate a random sequence of bits to be the key
		key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
		key_pool.append(key)  # add the key to the pool. the key index is its index on this list
	print("Generated pool of size: "+ str(len(key_pool)))
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
#	while(len(state.toSendKeys) == 0):
#		pass
#	time.sleep(20)
	print("Sending the keys to the Clients...")
#	for addrs in state.toSendKeys:
#		print("Sending to: "+ str(addrs))
#		messages.send_single_msg(messages.CLIENT_KEYS, addrs)
#		messages.send_header(2*KEY_SIZE, addrs)
#		for i in xrange(2):
#			key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
#			print(str(i)+ ": "+ key)
#			messages.send_data(key, addrs)
	
