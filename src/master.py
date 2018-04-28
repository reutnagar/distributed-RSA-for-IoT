from state import *
from global_data import state
#from math import *
import random, math, string, time
import messages


# memory size
M = 512
# The number of network&#39;s nodes
n = 100
# the probability where it is certainly true that two nodes have a connectivity
Pc = 0.9
# size of sub keys 
k = M / 8
# n' neighborhood size
nn = 30
c = 50 # ?? real constant
p = math.log(n, math.e)/n + c/n
d = p * (n - 1)
pp = d / (nn - 1) # p'
gP = -k**2/math.log(1-pp)
## need to define the func() correctly
# P = int(fsolve(func, gP)[0]) 
KEY_SIZE = 20

def calculate_pool_size():
	print("Master: Calculating  the pool size...")
	return 100 # only for DEBUG!!
	
def calculate_sub_keys_size():
	print("Master: Calculating  the subset size = " + str(k))
	return k
	
def generate_key_pool():
	print("Master: Generating the key pool")
	keyPool = []  # list of keys
	poolSize = 100 # for DEBUG!!
	for i in xrange(poolSize):
		# generate a random sequence of bits to be the key
		key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
		keyPool.append(key)  # add the key to the pool. the key index is its index on this list
	print("Generated pool of size: "+ str(len(keyPool)))
	return keyPool
	
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
	
