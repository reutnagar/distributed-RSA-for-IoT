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
		print("in findMaster. status is: "+ str(state.status)+" counter is: "+ str(counter))
		# ask if there is master on the network
		messages.broadcast(messages.IS_THERE_MASTER)
		# wait for master response (it takes a long time for the IoT to respond... ~10 seconds!)
		time.sleep(10)
		if(canIBeMaster):
			counter -= 1
			if(counter == 0 and state.status != MASTER_FOUND): # after 2 tries to find the master, set myself as Master
				messages.broadcast(messages.I_AM_MASTER)
				state.status =  MASTER_FOUND
				return True
	return False

def publishMe():
	messages.broadcast(messages.I_AM_ON_THE_NETWORK)
	print("Publish my IP on the network...")