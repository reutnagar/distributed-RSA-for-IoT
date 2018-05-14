from state import *
from global_data import *
import messages, client

print("**Node startup**")

#init()

# listen to every message from the network, and process it. will modify "state" if needed
messages.async_listen_to_messages()

state.status = NODE_INIT

# ask "who is Master" in the network. return True if I am the Master, False otherwise
state.IAmMaster = client.find_master()
print("in main. Master is found!")

if(state.IAmMaster): # perform Master logic
	import master
	state.status = MASTER_INIT
	
	# Master calculations
	state.poolSize = master.calculate_pool_size()
	state.subKeysSize = master.calculate_sub_keys_size()
	# generate the keys
	state.keys = master.generate_key_pool()
	# send the sub-pool keys
	print 'a'
	while(state.toSendKeys == []):
		pass
	print 'to_send_keys is not empty, there is an ip: ' + str(state.toSendKeys)
	master.send_keys(state)
	while(True):
		pass
	state.status = MASTER_DONE	
else: # client logic
	state.status = CLIENT_INIT
	# wait until key are sent from Master
	print("Waiting to receive the keys from the Master...")
	while(state.status != CLIENT_GOT_KEYS):  # now the code is stuck here!!
		pass
	print 'after recieving keys'
	print state.keys
	# publish my IP in the network
	client.publishMe()
	state.status = CLIENT_DONE	

# Secured network has been established, can continue other work...
#while(True)