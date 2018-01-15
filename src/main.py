import socket
import logging
import sys
import network
import time
from client import Client
from master import Master

logger = 0
IAmMaster = False

def init_log():
    FORMAT = '%(asctime)-15s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

def init():
    init_log()

def main():
    global IAmMaster
    init()

    logging.info('start service ...')

    try:
        while(not IAmMaster):
            client = Client()
            IAmMaster = client.run(4)
        master = Master()
        master.run()
    except KeyboardInterrupt:   # print all messages
        # print 'buffer: %s' %(str(client.buffer))
        sys.exit()

if __name__ == "__main__" :
    main()
