class Chatroom:
	def __init__(self):
		self.chatlog = []
	
	def get_chatlog(self):
		return self.chatlog
	
	def add_message(self, message):
		self.chatlog.append(message)
		
	def clear_chatlog(self):
		self.chatlog = []
