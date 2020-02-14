import random
import string
from datetime import datetime, timedelta

class user(object):
	def __init__(self, name, colour):
		self._name = name
		self._colour = colour
	
	def get_name(self):
		return self._name
	
	def get_colour(self):
		return self._colour
		
	def to_json(self):
		return {
			"name": self._name
			"colour": self._colour
		}
		
class chatroom(object):
	def __init__(self, name):
		self._id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
		self._name = name
		self._users = {}
		self._messages = []
		
	def add_user(self, user: user):
		if user.get_name() in self._users:
			raise KeyError
		self._users.update({user.get_name(): user})
	
	def get_all_users(self):
        return self._users.values()

    def get_user(self, user_name, default = None):
        return self._users.get(user_name, default)

class rooms(object):
	_instance = None
	
	def __init__(self):
		raise RuntimeError("Call get() instead")
	
	@classmethod
	def get_map(cls):
		if _instance is None:
			print("Creating gameroom map instance")
			cls._instance = {}
		return cls._instance
		
		
		
		
		
