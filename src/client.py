from state import *
from global_data import state
import messages
from messages import Message
import time, os

def find_master():
	print("Looking for the Master on the network...")
	counter = 2
	canIBeMaster = True # may be done with: calculateStrengh() function
	while(state.status != MASTER_FOUND):
		print("Trying for the #" + str(3-counter) + " time...")
		messages.broadcast(messages.IS_THERE_MASTER) # ask if there is master on the network
		time.sleep(10) # wait for master response (it takes a long time for the IoT to respond... ~10 seconds!)
		if(canIBeMaster): # if the node can be a master
			counter -= 1
			if(counter == 0 and state.status != MASTER_FOUND): # after 2 tries to find the master, set myself as Master
				messages.broadcast(messages.I_AM_MASTER)
				state.masterIP = state.myIP
				state.status =  MASTER_FOUND
				print("No master is found! Setting myself as master")
				return True
	return False

def publishMe():
	print("Publishing my IP on the network...")
	messages.broadcast(messages.I_AM_ON_THE_NETWORK)
