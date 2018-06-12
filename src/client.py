from state import *
from global_data import state
import messages
from messages import Message
import time, os

def find_master():
	print("Looking for the Master on the network...")
	counter = 2
	canIBeMaster = True # calculateStrengh()
	while(state.status != MASTER_FOUND):
		print("in findMaster. status is: "+ str(state.status)+" counter is: "+ str(counter))
		# ask if there is master on the network
		messages.broadcast(messages.IS_THERE_MASTER,0,None)
		# wait to master response (need to see how long is master initialization)
		if os.name == "nt": # for Windows PC
			time.sleep(10)
		elif os.name == "posix": # for Raspberry Pi
			time.sleep(0.5)	  
		
		if(canIBeMaster):
			counter -=1
			if(counter == 0 and state.status != MASTER_FOUND): # after 2 tries to find the master, set myself as Master
				messages.broadcast(messages.I_AM_MASTER, 0, None)
				state.status =  MASTER_FOUND
				return True
	return False

def publishMe():
	messages.broadcast(messages.I_AM_ON_THE_NETWORK, 0,None)
	print("Publish my IP on the network...")