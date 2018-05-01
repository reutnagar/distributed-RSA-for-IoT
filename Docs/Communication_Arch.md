
# Communication Arch
About messages structure see [here](https://github.com/reutnagar/distributed-RSA-for-IoT/blob/master/Docs/Massages_Structure_Arch.md)
## Listening to messages
will be done on a different thread to allow parallel execution of commands, and better response time for messages on the network.
```
stateInt  // save the state to be accesible for all functions

async_listenToMessages(state):
	stateInt = state
	thread.open(function = asyncListen)

asyncListen():
	while(True):  // may stop the thread on some codition...
		msg, ip = listen()  // block untill message accepted
		process_message(message, ip)
```

## Message Processing
The actions/ behavior that will be taken when the following messages are got:

- IS_THERE_MASTER: if status is MASTER_INIT or MASTER_DONE respond I_AM_MASTER. otherwise do nothing.
- I_AM_MASTER: if status is NODE_INIT, set status to be MASTER_FOUND and set the masterIP. if status is INIT do nothing. otherwise, raise error.
- I_AM_ON_THE_NETWORK: if the ip is not in neigbors list, add it.
- CLIENT_SUBSET_KEYS: if status is CLIENT_INIT, save the keys in the message. otherwise- raise error.

## Broadcast message in the network
```
broadcast(msg):
	send_msg(msg, "<broadcast>")
```

## Sending data in single message
```
send_msg(msg, ip):
	s = socket.open()
	header = struct.pack('>i', len(data))
	_send_block(s, header)
	_send_block(s, data)
```
## Sending data in multiple messages
```
global openedSocket
global openedSocketSize

send_header(size,ip):
	s = socket.open()
	header = struct.pack('>i', size)
	_send_block(s, header)
	openedSocket = s
	openedSocketSize = size

send_data(data,ip):
	_send_block(openedSocket, data)
	openedSocketSize -= len(data)
	if(openedSocketSize<= 0):
		openedSocket.close()		
```
