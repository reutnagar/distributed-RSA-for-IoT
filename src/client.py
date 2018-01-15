STATE_MASTER = 0
STATE_ERROR = -1
STATE_TMP_CLIENT = 1
STATE_CLIENT = 2

class Client():
	
	def __init__(self):
		self.state = STATE_CLIENT
		self.strengh = 6	# self.calc_strengh()

	def calc_strengh(self):
		pass

	def broadcast(self):
		#if(self.state != STATE_CLIENT)
		pass

	def listen(self):
		return ""

	def process_message(self, msg):
		pass

	def run(self,REQUIRED_STRENGH):		
		if(self.strengh > REQUIRED_STRENGH):
			self.state = STATE_TMP_CLIENT
			self.broadcast()
		while((self.state is not STATE_MASTER) and (self.state is not STATE_ERROR)):
			msg = self.listen()
			self.process_message(msg)
		if(self.state == STATE_MASTER):
			return True
		return False