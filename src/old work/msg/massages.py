import struct

def _get_block(s, count):
    if count <= 0:
        return ''
    buf = ''
    while len(buf) < count:
        buf2 = s.recv(count - len(buf))
        if not buf2:
            # error or just end of connection?
            if buf:
                raise RuntimeError("underflow")
            else:
                return ''
        buf += buf2
    return buf

def _send_block(s, data):
    while data:
        data = data[s.send(data):]

#if False:
def get_msg(s):
    count = struct.unpack('>i', _get_block(s, 4))[0]
    return _get_block(s, count)

def send_msg(s, data):
    header = struct.pack('>i', len(data))
    _send_block(s, header)
    _send_block(s, data)
    print '1'+header
    print '2'+data

# if True:

#     def _get_count(s):
#         buf = ''
#         while True:
#             c = s.recv(1)
#             if not c:
#                 # error or just end of connection/
#                 if buf:
#                     raise RuntimeError("underflow")
#                 else:
#                     return -1
#             if c == '|':
#                 return int(buf)
#             else:
#                 buf += c

#     def get_msg(s):
#         return _get_block(s, _get_count(s))

#     def send_msg(s, data):
#         _send_block(s, str(len(data)) + '|')
#         _send_block(s, data)


import threading
import socket
import time

def client(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.0.0.0', port))
    print get_msg(s)
    print get_msg(s)
    s.shutdown(socket.SHUT_RDWR)
    s.close()

def server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('10.0.0.0', port))
    s.listen(1)
    c, addr = s.accept()
    send_msg(c, 'hello')
    send_msg(c, 'there')
    c.close()
    s.close()

if __name__ == '__main__':
    c = threading.Thread(target=server, args=(9999,))
    c.start()
    time.sleep(1)
    client(9999)
    c.join()
    print 'done'