import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# === Classes ===

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
	
	def get_user_room(self, username):
		return self.users[username]

	# = Room Functionality =

	def create_room(self, name):
		chatroom_to_add = Chatroom()
		rooms.add_room(name, chatroom_to_add)

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

	# = User-Room Functionality =

	def add_user(self, username):
		self.change_user_room(username, "General")

	def change_user_room(self, username, room):
		if (room in self.rooms):
			self.users[username] = room
			rooms.add_message_to_room(room, "ADMIN", "User " + username + " joined the channel: " + room)
		else:
			print("Room does not exist: " + room)
			rooms.add_message_to_room(rooms.get_user_room(username), "ADMIN", "Room '" + room + "' does not exist.")

	# = Command Parsing =

	def parse_command(self, command, arguments, username):
		if(command == "help"):
			self.add_message_to_room(self.users[username], "COMMAND", "help, room (list/create/join) (room name)")
		elif (command == "room"):
			if (arguments[0] == "list"):
				self.add_message_to_room(self.users[username], "COMMAND", self.get_rooms())
			elif (arguments[0] == "create"):
				self.create_room(arguments[1])
			elif (arguments[0] == "join"):
				self.change_user_room(username, arguments[1])
		else:
			self.add_message_to_room(self.users[username], "COMMAND", "Invalid command. Try /help")

class Chatroom:
	def __init__(self):
		self.chatlog = []
	
	def get_chatlog(self):
		return self.chatlog
	
	def add_message(self, message):
		self.chatlog.append(message)

# === Global Variables ===

rooms = Rooms()

# === Routes ===

# == Post ==

@app.route('/chatroom/sendmessage/', methods=["POST"])
def receive_message():
    response = request.get_json()

    print(response)

    json_as_dict = convert_json_to_dict(response)
    user_room = rooms.get_user_room(json_as_dict["username"])
    rooms.add_message_to_room(user_room, json_as_dict["username"], json_as_dict["message"])

	# Commands
    if (json_as_dict["message"][0] == '/'):
        print("Command received.")
        command_to_give = str(json_as_dict["message"][1:])
        print(command_to_give)
        command_to_give = command_to_give.split()
        rooms.parse_command(command_to_give[0], command_to_give[1:], json_as_dict["username"])
    
    
    return jsonify(response)
    
@app.route('/chatroom/join/', methods=["POST"])
def set_user():
	response = request.get_json()
	json_as_dict = convert_json_to_dict(response)

	rooms.add_user(json_as_dict["username"])

	print(response)
	return jsonify(response)

# == Get ==

@app.route('/chatroom/chatlog/<username>/', methods=["GET"])
def get_chatlog(username):
	return jsonify(rooms.get_chatlog_from_room(username))

# == Flask Helpers ==

@app.after_request
def add_headers(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	return response

# === Utility ===

def convert_json_to_dict(json_to_convert):
	json_as_str = json.dumps(json_to_convert)
	json_as_dict = json.loads(json_as_str)
	return json_as_dict

# === Main ===

if __name__ == '__main__':
	rooms.create_room('General')

	app.run()
	#app.run(debug=True)		
