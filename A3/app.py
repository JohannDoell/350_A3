import json
from flask import Flask, request, jsonify

app = Flask(__name__)

chatlog = []

@app.route('/rooms/<room>/sendmessage/', methods=["POST"])
def receive_message(room):
    response = request.get_json()
    print(response)
    json_as_str = json.dumps(response)
    json_as_dict = json.loads(json_as_str)
    message_to_append = json_as_dict["username"] + ": " + json_as_dict["message"]
    chatlog.append(message_to_append)
    return jsonify(response)
    
@app.route('/user/setuser/', methods=["POST"])
def set_user():
	response = request.get_json()
	print(response)
	return jsonify(response)

@app.route('/rooms/<room>/chatlog/', methods=["GET"])
def get_chatlog(room):
	return jsonify(chatlog)
	#return room + " Chatlog"

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response
    
if __name__ == '__main__':
    app.run(debug=True)

class Rooms:
	rooms = {}
	
	def __init__(self):
		rooms = {}
	
	def get_room(name):
		return rooms[name]
	
	def add_room(name, room):
		rooms[name] = room
		
	def remove_room(name):
		del rooms[name]

class Chatroom:
	chatlog = []
	
	def __init__(self):
		self.chatlog = []
	
	def get_chatlog():
		return chatlog
	
	def add_message(message):
		self.chatlog.append(message)
		
