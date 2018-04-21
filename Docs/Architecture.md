# The new Arch for our Project

```
init()

// This holds all data about this node's state
state = State()

// listen to every message from the network, and process it. will modify "state" if needed
messages.async_listenToMessages(state)

state.status = NODE_INIT

// ask "who is Master" in the network. return True if I am the Master, False otherwise
state.IAmMaster = client.findMaster(state)

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
	
// do other stuff..
while(True)	
```
