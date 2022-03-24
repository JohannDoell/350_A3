import chatroom

class Rooms:	
	def __init__(self):
		self.rooms = {}
		self.users = {}
	
	# = Getters =

	def get_room(self, name):
		return self.rooms[name]
	
	def get_rooms(self):
		keys = ""
		for key in self.rooms.keys():
			keys += key + ", "
		return keys
	
	def get_rooms_as_list(self):
		keys = []
		for key in self.rooms.keys():
			keys.append(key)
		return keys
	
	def get_user_room(self, username):
		return self.users[username]

	# = Room Functionality =

	def create_room(self, name):
		chatroom_to_add = chatroom.Chatroom()
		self.add_room(name, chatroom_to_add)

	def add_room(self, name, room):
		if (name not in self.rooms):
			self.rooms[name] = room
		else:
			print("Cannot have duplicate rooms")
		
	def remove_room(self, name):
		if (name == "General"):
			print("Cannot delete the general channel")
		else:
			del self.rooms[name]

	def add_message_to_room(self, room_name, username, message):
		if (username != "ADMIN" and username != "COMMAND"):
			self.rooms[self.users[username]].add_message(username + ": " + message)
		else:
			self.rooms[room_name].add_message(username + ": " + message)

	def get_chatlog_from_room(self, username):
		return self.rooms[self.users[username]].get_chatlog()
		#return self.rooms[room_name].get_chatlog()
		
	def clear_room_chatlog(self, username):
		self.rooms[self.users[username]].clear_chatlog();

	# = User-Room Functionality =

	def add_user(self, username):
		self.change_user_room(username, "General")

	def change_user_room(self, username, room):
		if (room in self.rooms):
			self.users[username] = room
			self.add_message_to_room(room, "ADMIN", "User " + username + " joined the channel: " + room)
		else:
			print("Room does not exist: " + room)
			self.add_message_to_room(rooms.get_user_room(username), "ADMIN", "Room '" + room + "' does not exist.")

	# = Command Parsing =

	def parse_command(self, command, arguments, username):
		if(command == "help"):
			self.add_message_to_room(self.users[username], "COMMAND", "help, room (list/create/join) (room name), clear")
		elif (command == "room"):
			if (arguments[0] == "list"):
				self.add_message_to_room(self.users[username], "COMMAND", self.get_rooms())
			elif (arguments[0] == "create"):
				self.create_room(arguments[1])
			elif (arguments[0] == "join"):
				self.change_user_room(username, arguments[1])
			elif (arguments[0] == "delete"):
				# Delete the room.
				pass
			else:
				self.add_message_to_room(self.users[username], "COMMAND", "Invalid command. Try /help")
		elif (command == "clear"):
			self.clear_room_chatlog(username)
		else:
			self.add_message_to_room(self.users[username], "COMMAND", "Invalid command. Try /help")

