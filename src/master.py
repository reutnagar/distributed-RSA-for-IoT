from state import *
#from math import *
import random, math, string

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

def calculatePoolSize(state):
	print("Master: Calculating  the pool size...")
	
def calculateSubKeysSize(state):
	print("Master: Calculating  the subset size = " + str(k))
	return k
	
def generateKeyPool(state):
	print("Master: Generating the key pool")
	keyPool = []  # list of keys
	poolSize = 100 # for DEBUG!!
	for i in xrange(poolSize):
		# generate a random sequence of bits to be the key
		key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
		keyPool.append(key)  # add the key to the pool. the key index is its index on this list
	print("Generated pool of size: "+ str(len(keyPool)))
	return keyPool
	
def sendKeys(state):
	print("Sending the keys to the Clients...")
