# Client Architecture

## Calculating The Node's Strengh
```
MIN_MEMORY = 500 // to be decided later..
MIN_STORAGE = 500 // to be decided later..
MIN_TRANS = 500 // to be decided later..
MIN_CPU = 500 // to be decided later..
calculateStrengh():
	memory, storage, transmition_rate, cpu
	return (memory >= MIN_MEMORY && storage >= MIN_STORAGE && transmition_rate >= MIN_TRANS && cpu >= MIN_CPU)
```
## Finding The Master in The Network
A node will have 3 states:
1. It can not be a Master (canIBeMaster = False): will stuck in this loop untill the Master will respond. 
			return False
2. There is another Master on the network: it will probably get response from the Master within the timeout in 2 tries. return False
3. if non of the above: will set myself as master of the network. return True
```
findMaster(state):
	counter = 2
	canIBeMaster = calculateStrengh()
	while(state.status != MASTER_FOUND):
		// ask if there is master on the network
		message = IS_THERE_MASTER
		broadcast(message)
		timeout(2)  // wait to master response (need to see how long is master initialization)
		
		if(canIBeMaster):
			counter--
			if(counter == 0): // after 2 tries to find the master, set myself as Master
				message = I_AM_MASTER
				broadcast(message)
				state.status =  MASTER_FOUND
				return True
	return False
```
## Generate Asymetric key pair
```
generate_RSA_key():
		
```
## Send Public key
```
send_public_key_to_master():
	public = state.publicKey
	messages.send_single_message(CLIENT_PUBLIC_KEY, public)
```
## Publish The Node IP
```
publishMe():
	message = I_AM_ON_THE_NETWORK
	broadcast(message)
```
