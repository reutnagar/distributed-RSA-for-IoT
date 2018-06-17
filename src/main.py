from state import *
from global_data import *
import messages, client, crypt
import time

print("**Node startup**")

# listen, in other thread, to every message from the network, and process it. will modify "state" if needed
messages.async_listen_to_messages()

state.status = NODE_INIT

# ask "who is Master" in the network. 
# return True if I am the Master, False otherwise
state.IAmMaster = client.find_master()
print("Master is found! master ip is: " + str(state.masterIP))

if(state.IAmMaster): # perform Master logic
	import master
	state.status = MASTER_INIT
	
	# Master calculations
	state.poolSize = master.calculate_pool_size()
	print("Calculated the pool size. The size is: " + str(state.poolSize))
	state.subKeysSize = master.calculate_sub_keys_size()
	print("Calculated the sub pool size. The size is: " + str(state.subKeysSize))

	# generate the keys
	state.pool_keys = master.generate_key_pool()
	for index, key in enumerate(state.pool_keys):
		state.keys.append((index,key))
	#print("my keys: "+str(state.keys))
	# send the sub-pool keys
	while(state.toSendKeys != []):
		master.send_keys()
	state.status = MASTER_DONE
	
	
else: # perform client logic
	state.status = CLIENT_INIT
	#generate RSA key
	print("Generating RSA key...")
	state.RSAPublic, state.RSAPrivate = crypt.generate_asym_key()
	# send client public key to master
	messages.send_single_msg(state.masterIP, 'CLIENT_PUBLIC_KEY', 2048, state.RSAPublic)

	# wait until key are sent from Master
	print("Waiting to receive the keys from the Master...")
	while(state.status != CLIENT_GOT_KEYS):  
		pass
	print('Recieved the keys from the master. Now decrypting... ')
	# decrypt all the keys
	state.keys = [(index, crypt.decrypt_asym(state.RSAPrivate, key)) for (index, key) in state.keys]
	print("Got "+ str(len(state.keys)) +" keys, My indexes are: "+ str([x[0] for x in state.keys]))
	# publish my IP in the network
	client.publishMe()
	state.status = CLIENT_DONE
	# Send messages using the common index- if there is...
	stop = False
	while(stop != True):
		for neighbor, index in state.neighbors:
			if index != -1 and neighbor != state.masterIP:
				time.sleep(20) # not to overload the network... 
				# Find the common index of me and the neighbor
				key = ''.join([key for (i, key) in state.keys if i == index])
				msg = "This is a very secret message from: "+ state.myIP
				print("The message is: " + str(msg))
				# Encrypt the message with AES (key is 256 bit)
				iv, cipher = crypt.encrypt_message(key, msg)
				print("The cipher is: "+ str(cipher))
				messages.send_single_msg(neighbor, messages.MESSAGE_ENC_DATA, iv, cipher)
				stop = True


# Secured network has been established, can continue other work...
while(True):
	pass
