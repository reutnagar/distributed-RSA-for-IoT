import socket
import logging
import sys
#import network
import time
from global_defs import *
from internal_state import InternalState
from client import Client
from master import Master

logger = 0

def init_log():
    FORMAT = '%(asctime)-15s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

def init():
    init_log()

def main():
    my_state = InternalState()
    init()

    logging.info('start service ...')

    try:
        while(my_state.state is not STATE_MASTER):
            client = Client()
            my_state = client.run(4, my_state)
        master = Master()
        master.run()
    except KeyboardInterrupt:   # print all messages
        # print 'buffer: %s' %(str(client.buffer))
        sys.exit()

if __name__ == "__main__" :
    main()
