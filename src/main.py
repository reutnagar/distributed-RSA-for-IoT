from state import *
from global_data import state
import messages, master, client

print("**Node startup**")

# init()

# listen to every message from the network, and process it. will modify "state" if needed
#messages.async_listenToMessages(state)
messages.async_listenToMessages(state)

state.status = NODE_INIT

# ask "who is Master" in the network. return True if I am the Master, False otherwise
state.IAmMaster = client.findMaster(state)
print("in main. Master is found!")

if(state.IAmMaster): # perform Master logic
	state.status = MASTER_INIT
	while(state.status == MASTER_INIT):
		pass
	# Master calculations
	state.poolSize = master.calculatePoolSize(state)
	state.subKeysSize = master.calculateSubKeysSize(state)
	# generate the keys
	state.keys = master.generateKeyPool(state)
	# send the sub-pool keys
	master.sendKeys(state)
	state.status = MASTER_DONE	
else: # client logic
	state.status = CLIENT_INIT
	# wait until key are sent from Master
	print("Waiting to receive the keys from the Master...")
	while(state.status != CLIENT_GOT_KEYS):  # now the code is stuck here!!
		pass
	# publish my IP in the network
	client.publishMe()
	state.status = CLIENT_DONE	

# Secured network has been established, can continue other work...
#while(True)