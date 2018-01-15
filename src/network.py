import asyncore, socket
import threading


class MessageProcessor(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.bind(('',8881))
        self.buffer = ""

        # self.connect( (host, 80) )

    def handle_connect(self):
        pass

    def handle_close(self):
        pass
        #self.close()

    def handle_read(self):
        message , address = self.recvfrom(8192)
        self.buffer = self.buffer +'\n'+ message
        print 'message %s from : %s' % ( str(message), address[0])

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

def start():
    client = MessageProcessor('www.python.org', '/')
    comm = threading.Thread(target=asyncore.loop)
    comm.daemon = True
    comm.start()
    return client
# # asyncore.loop()
# x = 0
# while True:
#     x = x+1
#     print 'number: %d' % (x)
#     time.sleep(1)