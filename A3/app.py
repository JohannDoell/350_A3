import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class Rooms:	
	def __init__(self):
		self.rooms = {}
	
	def get_room(self, name):
		return self.rooms[name]
	
	def get_rooms(self):
		keys = ""
		for key in self.rooms.keys():
			keys += key + ", "
		return keys

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
		self.rooms[room_name].add_message(username + ": " + message)

	def get_chatlog_from_room(self, room_name):
		return self.rooms[room_name].get_chatlog()

	def parse_command(self, room, command, arguments):
		if(command == "help"):
			self.add_message_to_room(room, "COMMAND", "help, listrooms, createroom (name), joinroom (name)")
		elif (command == "listrooms"):
			self.add_message_to_room(room, "COMMAND", self.get_rooms())
		elif (command == "createroom"):
			self.create_room(arguments[0])
		elif (command == "joinroom"):
			pass

class Chatroom:
	def __init__(self):
		self.chatlog = []
	
	def get_chatlog(self):
		return self.chatlog
	
	def add_message(self, message):
		self.chatlog.append(message)
	
rooms = Rooms()

@app.route('/rooms/<room>/sendmessage/', methods=["POST"])
def receive_message(room):
    response = request.get_json()

    json_as_dict = convert_json_to_dict(response)
    rooms.add_message_to_room(room, json_as_dict["username"], json_as_dict["message"])

	# Commands
    if (json_as_dict["message"][0] == '/'):
        print("Command received.")
        command_to_give = str(json_as_dict["message"][1:])
        print(command_to_give)
        command_to_give = command_to_give.split()
        rooms.parse_command(room, command_to_give[0], command_to_give[1:])
    
    print(response)
    return jsonify(response)
    
@app.route('/rooms/<room>/join/', methods=["POST"])
def set_user(room):
	response = request.get_json()
	json_as_dict = convert_json_to_dict(response)

	rooms.add_message_to_room(room, "ADMIN", "User " + json_as_dict["username"] + " joined the channel.")

	print(response)
	return jsonify(response)

@app.route('/rooms/<room>/chatlog/', methods=["GET"])
def get_chatlog(room):
	return jsonify(rooms.get_chatlog_from_room(room))

@app.after_request
def add_headers(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	return response

def convert_json_to_dict(json_to_convert):
	json_as_str = json.dumps(json_to_convert)
	json_as_dict = json.loads(json_as_str)
	return json_as_dict


if __name__ == '__main__':
	rooms.create_room('General')

	app.run()
	#app.run(debug=True)		
