## status Definition ##
INIT = 0
NODE_INIT = 1
MASTER_FOUND = 2
#only for Master
MASTER_INIT = 3
MASTER_DONE = 4
#only for Client
CLIENT_INIT = 5
CLIENT_GETTING_KEYS = 6
CLIENT_GOT_KEYS = 7
CLIENT_DONE = 8

class State(object):
	
	status = INIT # hold the current state/ status of the node in the network
	IAmMaster = False # whether this node is the Master
	
	neighbors = []  # list of known neighbors on the network
	myKeys = []  # list of my sub pool of keys, with their indexes
	masterIP = "" # will hold the IP of the Master on the network
	
	# only relevant to Master:
	poolSize = 0 # the size of the keys pool to be generated
	subKeysSize = 0 # the size of the sub key-pool to be sent to each node
	keys = [] # the key pool
	toSendKeys = [] # list of IPs that the Master will send key to after generation of the key is done
