from global_defs import *

class InternalState():
	
	def __init__(self):
		self.state = STATE_INIT
		self.net_state = NET_STATE_INIT
		self.master_ip = ""
		self.neighbors = []
		self.strengh = 0