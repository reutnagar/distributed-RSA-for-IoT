from state import *
from global_data import state
import messages
import time

def findMaster(state):
	print("Looking for the Master on the network...")
	counter = 2
	canIBeMaster = True # calculateStrengh()
	while(state.status != MASTER_FOUND):
		print("in findMaster. status is: "+ str(state.status)+" counter is: "+ str(counter))
		# ask if there is master on the network
		message = messages.IS_THERE_MASTER
		messages.broadcast(message)
		time.sleep(0.5)  # wait to master response (need to see how long is master initialization)
		
		if(canIBeMaster):
			counter -=1
			if(counter == 0 and state.status != MASTER_FOUND): # after 2 tries to find the master, set myself as Master
				message = messages.I_AM_MASTER
				messages.broadcast(message)
				state.status =  MASTER_FOUND
				return True
	return False

def publishMe():
	print("Publish my IP on the network...")