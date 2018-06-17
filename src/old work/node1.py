#!/usr/bin/python

import socket
import struct
import thread
import time
import sys

# connect to leader and retrive key

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

sub_keys = {}

connected = []

try:
    print 'Connect to leader and recv keys...'
    dlen = struct.unpack('<I', sock.recv(4))[0]
    print 'dlen=', dlen
    keys = sock.recv(dlen).split(';')
    for k in keys:
        if k is '':
            continue
        id = k.split(':')[0]
        sub_keys[int(id)] = k.split(':')[1]
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

print 'subKeys=', sub_keys

# bind a server and wait other node to connect
def node_auth(sock):
    global sub_keys
    dlen = struct.unpack('<I', sock.recv(4))[0]
    index_list = sock.recv(dlen).split(':')
    print 'index_list =', index_list
    for i in index_list:
        i = int(i)
        if i in sub_keys:
            data = str(i) + ':' + sub_keys[i]
            sock.sendall(struct.pack('<I', len(data)) + data)
            dlen = struct.unpack('<I', sock.recv(4))[0]
            data = sock.recv(dlen)
            if data is 'Finish':
                return True
    sock.close()
    return False

def bind():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10001)
    print 'bind server...', server_address
    sock.bind(server_address)
    while True:
        try:
            sock.listen(1)
            conn, cleint_addr = sock.accept()
            print 'Connection from', cleint_addr
            try:
                for i in xrange(5): # try 5 times
                    res = node_auth(conn)
                    if res:
                        print "Auth Success to ", cleint_addr
                        break
                    else:
                        print 'Auth Fail retry...', i+1
            finally:
                print cleint_addr, 'is closed.'
                conn.close()
        except:
            pass

thread.start_new_thread(bind, ())
# connect to other node

while True:
    time.sleep(1)