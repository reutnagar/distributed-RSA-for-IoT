# The new Arch for our Project
This document will describe the functionality of the main module of our progarm. This is the first code that will be run on a node in the IoT Network, and will invoke othe modules/ functions.
Other modules are: master, client, messages, state.

## Initialization
On reset a node will initialize it internal state and variable.
Then will listen to every message on the network, asynchronous. This is done to make sure the node does not miss any message about a master exist on the network, or to prevent timing issues that can occure.
At this phase its status is INIT. see explenation [here](https://github.com/reutnagar/distributed-RSA-for-IoT/blob/master/Docs/State_Arch.md).
```
init()

// This holds all data about this node's state
state = State()

// listen to every message from the network, and process it. will modify "state" if needed
messages.async_listenToMessages(state)
```

## Finding the Master on The Network
A node will ask if there is a master on the ntwok and will wait for reply. see more [here](https://github.com/reutnagar/distributed-RSA-for-IoT/blob/master/Docs/Client_Arch.md)
```
state.status = NODE_INIT

// ask "who is Master" in the network. return True if I am the Master, False otherwise
state.IAmMaster = client.findMaster(state)
```
## Master and Client operations
See more about Master operations [here](https://github.com/reutnagar/distributed-RSA-for-IoT/blob/master/Docs/Master_Arch.md), and about Client's [here](https://github.com/reutnagar/distributed-RSA-for-IoT/blob/master/Docs/Client_Arch.md)
```
if(state.IAmMaster): // perform Master logic
	state.status = MASTER_INIT
	// Master calculations
	state.poolSize = master.calculatePoolSize(state)
	state.subKeysSize = master.calculateSubKeysSize(state)
	// generate the keys
	state.keys = master.generateKeyPool(state.poolSize)
	// send the sub-pool keys
	master.sendKeys(state)
	state.status = MASTER_DONE	
else: // client logic
	state.status = CLIENT_INIT
	// wait untill key are sent from Master
	while(state.status != CLIENT_GOT_KEYS)
	// publish my IP in the network
	client.publishMe()
	state.status = CLIENT_DONE	
```
### After These Actions, The IoT network is secured, and nodes can communicate with privacy 
```
// do other stuff..
while(True)	
```
