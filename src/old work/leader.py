#!/usr/bin/python
from scipy.optimize import fsolve
from math import log
import random
import string
import math
import socket
import thread
import struct
import time
import sys


# function to calculate p'
def func(P):
    global pp
    global k
    return log(1-pp)-(2*P-2*k+1)*log(1-k/P)+(P-2*k+0.5)*log(1-2*k/P)


def generate_sub_keys(key_pool, k):
    sub_keys = {}
    for i in xrange(k):
        id = -1
        while id < 0 or id in sub_keys:
            id = int(math.floor(random.random() * len(key_pool)))
        sub_keys[id] = key_pool[id]
    return sub_keys

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
c = 50 # ?? 
p = log(n, math.e)/n + c/n
d = p * (n - 1)
pp = d / (nn - 1)
gP = -k**2/log(1-pp)
P = int(fsolve(func, gP)[0])

print 'k=', k
print 'd=', d
print 'pp=', p
print 'P=', P
print 'generate keypool...'
key_pool = {}
for i in xrange(P):
    key_pool[i] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

# wait and send key to node
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)

while True:
    try:
        sock.listen(1)
        print 'waiting for a connection'
        connection, client_address = sock.accept()
        print 'connection from', client_address
        # TODO : auth
        print 'send sub keys...'
        sub_keys = generate_sub_keys(key_pool, k)
        data = ''
        for i in sub_keys:
            data = data + str(i) + ':' + sub_keys[i] + ';'
        print 'data=', data
        connection.sendall(struct.pack("<I", len(data)))
        connection.sendall(data)
        connection.close()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass

