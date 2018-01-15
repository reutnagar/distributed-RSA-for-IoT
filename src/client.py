import socket
import sys


def main(message) :
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    my_socket.sendto("wearetherock", ('<broadcast>' ,8881))
    my_socket.close()


if len(sys.argv) < 2 :
	print 'use: python tomboy_client.py "message"'
else :
    main(sys.argv[1])
