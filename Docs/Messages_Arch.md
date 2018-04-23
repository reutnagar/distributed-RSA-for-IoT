

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
