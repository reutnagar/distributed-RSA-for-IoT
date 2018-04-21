# State Arch

```
class State(object):
	
	status = INIT // hold the current state/ status of the node in the network
	IAmMaster = False // whether this node is the Master
	
	neighbors = []  // list of known neighbors on the network
	myKeys = []  // list of my sub pool of keys, with their indexes
	
	// only relevant to Master:
	poolSize = 0 // the size of the keys pool to be generated
	subKeysSize = 0 // the size of the sub key-pool to be sent to each node
	keys = [] // the key pool
	toSendKeys = [] // list of IPs that the Master will send key to after generation of the key is done
	
```
