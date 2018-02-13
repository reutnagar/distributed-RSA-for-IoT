from global_defs import *

class InternalState():
	
	def __init__(self):
		self.state = STATE_INIT
		self.master_ip = ""
		self.neighbors = []