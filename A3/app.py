import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class Rooms:	
	def __init__(self):
		self.rooms = {}
	
	def get_room(self, name):
		#print(self.rooms)
		return self.rooms[name]
	
	def add_room(self, name, room):
		#print(self.rooms)
		self.rooms[name] = room
		#print(self.rooms)
		
	def remove_room(self, name):
		del self.rooms[name]

class Chatroom:
	def __init__(self):
		self.chatlog = ["Test1"]
	
	def get_chatlog(self):
		return self.chatlog
	
	def add_message(self, message):
		self.chatlog.append(message)

rooms = Rooms()

@app.route('/rooms/<room>/sendmessage/', methods=["POST"])
def receive_message(room):
    response = request.get_json()
    print(response)
    
    json_as_str = json.dumps(response)
    json_as_dict = json.loads(json_as_str)
    
    message_to_append = json_as_dict["username"] + ": " + json_as_dict["message"]
    chatlog.append(message_to_append)
    
    return jsonify(response)
    
@app.route('/rooms/<room>/join/', methods=["POST"])
def set_user(room):
	response = request.get_json()
	print(response)
	return jsonify(response)

@app.route('/rooms/<room>/chatlog/', methods=["GET"])
def get_chatlog(room):
	room_name = room
	room_to_get = rooms.get_room(room_name)
	chatlog_to_return = room_to_get.get_chatlog()
	return jsonify(chatlog_to_return)

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
	chatroom_to_add = Chatroom()
    
	rooms.add_room('General', chatroom_to_add)

	app.run(debug=True)		
