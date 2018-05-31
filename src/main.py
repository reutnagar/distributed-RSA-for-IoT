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
	state.status = MASTER_DONE
	index1= [22,1,4,0,5,44]
	print(index1)
	#state.keys.append(index1)
	
	
else: # client logic
	state.status = CLIENT_INIT
	# send public key to master
	#messages.send_single_msg('CLIENT_PUBLIC_KEY',0,None, state.masterIP)
	messages.broadcast('CLIENT_PUBLIC_KEY',0,None)
	#messages.send_single_msg('CLIENT_PUBLIC_KEY',0,None,state.masterIP)
	print('send msg CLIENT_PUBLIC_KEY to: '+str(state.masterIP)+' now its broadcast')

	# wait until key are sent from Master
	print("Waiting to receive the keys from the Master...")
	while(state.status != CLIENT_GOT_KEYS):  
		pass
	print 'after recieving keys'
	print state.keys
	# publish my IP in the network
	client.publishMe()
	state.status = CLIENT_DONE
	print('end client, now')
	index2 = [2,7,3,4,9,23]
	ip1 = '10.0.0.6'
	#messages.send_single_msg(messages.CLIENT_START_SESSION,0,index2,ip1)
	messages.broadcast(messages.CLIENT_START_SESSION,0,index2)
	print('send list of indexes: '+str(index2))

# Secured network has been established, can continue other work...
while(True):
	pass