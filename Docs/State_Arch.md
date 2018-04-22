# State Arch
## Status Of A Node in The Network
A node's status will determine its current phase in the process of establishing secured connection on the IoT network. It will be used to sync between the asynchronous thread that handles incoming messages and the main thread.
The following statuses are defined:
-  INIT: The node did to perform any operation on the network
-  NODE_INIT: The node started listening to incoming messages on the network, and will process them
-  MASTER_FOUND: The master on the is known to the node. the master can be either another node or itself

<b> Statuses that are relevant for Master only</b>
-  MASTER_INIT: The Node is performing the operations to create the keys pool
-  MASTER_DONE:	The node has completed the keys creation and sent them to the available Client nodes on the network

<b> Statuses that are relevant for Client only</b>
-  CLIENT_INIT: The node is waiting the get from the Master a subset of keys from the keys pool
-  CLIENT_GOT_KEYS: The client got its subset of keys and their indexes
-  CLIENT_DONE: The client discovered itself to the network members.

## State Class
This class will hold all the node's data that is required to be shared between the two threads, and will availble for reading and writing across the files/functions.
```
class State(object):
	
	status = INIT // hold the current state/ status of the node in the network
	IAmMaster = False // whether this node is the Master
	
	neighbors = []  // list of known neighbors on the network
	myKeys = []  // list of my sub pool of keys, with their indexes
	masterIP = "" // will hold the IP of the Master on the network
	
	// only relevant to Master:
	poolSize = 0 // the size of the keys pool to be generated
	subKeysSize = 0 // the size of the sub key-pool to be sent to each node
	keys = [] // the key pool
	toSendKeys = [] // list of IPs that the Master will send key to after generation of the key is done
	
```
