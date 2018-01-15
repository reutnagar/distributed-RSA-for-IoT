import socket
import logging
import sys
import network
import time

logger = 0

def init_log():
    FORMAT = '%(asctime)-15s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

def init():
    pass

def main():
    init_log()
    init()

    # my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # my_socket.bind(('',8881))
    logging.info('start service ...')

    try:
        # while True :
        #     message , address = my_socket.recvfrom(8192)
        #     logging.info('message %s from : %s' % ( str(message), address[0]))
        client = network.start()    
        x = 0
        while True: # Async read from socket, can perform other operations here...
            x = x+1
            print 'number: %d' % (x)
            time.sleep(1)
    except KeyboardInterrupt:   # print all messages
        print 'buffer: %s' %(str(client.buffer))
        sys.exit()

if __name__ == "__main__" :
    main()
