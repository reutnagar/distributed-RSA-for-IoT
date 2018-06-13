from state import *
from global_data import *
import messages, client, crypt
import time

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
	state.pool_keys = master.generate_key_pool()
	for index, key in enumerate(state.pool_keys):
		state.keys.append((index,key))
	#state.keys = [(1,'frergef'),(55,'regfghg'),(34,'kkkkk')] #only for testing!!
	print("my keys: "+str(state.keys))
	# send the sub-pool keys
	while(state.toSendKeys != []):
		master.send_keys()
	print("Finished sending the keys to all registered clients!")	
	state.status = MASTER_DONE
	
	
else: # client logic
	state.status = CLIENT_INIT
	# send client public key to master
	state.RSAPublic, state.RSAPrivate = crypt.generate_asym_key()
	messages.send_single_msg(state.masterIP, 'CLIENT_PUBLIC_KEY', 2048, state.RSAPublic)
	print('Sent public key to Master : ' + str(state.masterIP))

	# wait until key are sent from Master
	print("Waiting to receive the keys from the Master...")
	while(state.status != CLIENT_GOT_KEYS):  
		pass
	print('after recieving keys: ')
	print(state.keys)
	# decrypt all the keys
	state.keys = [(index, crypt.decrypt_asym(state.RSAPrivate, key)) for (index, key) in state.keys]
	# publish my IP in the network
	client.publishMe()
	state.status = CLIENT_DONE
	print('end client, now')
	print('send list of indexes: '+str(state.keys))

# send few messages with the common index- if there is...
while(True):
	for neighbor, index in state.neighbors:
		if index != -1:
			time.sleep(50) # not to overload the network...
			key = ''.join([key for (i, key) in state.keys if i == index]) # supposed to find only one key with the same index!
			msg = "This is a very secret message from: "+ state.myIP
			print("message sent is: " + str(msg))
			iv, cipher = crypt.encrypt_message(key, msg)
			messages.send_single_msg(neighbor, messages.MESSAGE_ENC_DATA, iv, cipher)
# Secured network has been established, can continue other work...
while(True):
	pass