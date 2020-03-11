import json
from flask import Flask, request, jsonify

import rooms

app = Flask(__name__)

# === Classes ===

# === Global Variables ===

chat = rooms.Rooms()

# === Routes ===

# == Post ==
    
@app.route('/chatroom/register/', methods=["POST"])
def register_user():
	response = request.get_json()
	json_as_dict = convert_json_to_dict(response)

	chat.add_user(json_as_dict["username"])

	print(response)
	return jsonify(response)

@app.route('/chatroom/sendmessage/', methods=["POST"])
def receive_message():
    response = request.get_json()

    print(response)

    json_as_dict = convert_json_to_dict(response)


	# Commands
    if (json_as_dict["message"][0] == '/'):
        print("Command received.")
        command_to_give = str(json_as_dict["message"][1:])
        print(command_to_give)
        command_to_give = command_to_give.split()
        chat.parse_command(command_to_give[0], command_to_give[1:], json_as_dict["username"])
    else:
        user_room = chat.get_user_room(json_as_dict["username"])
        chat.add_message_to_room(user_room, json_as_dict["username"], json_as_dict["message"])
    
    
    return jsonify(response)

@app.route('/chatroom/command/', methods=["POST"])
def receive_command():
	response = request.get_json()
	print(response)

	json_as_dict = convert_json_to_dict(response)


# == Get ==

@app.route('/chatroom/chatlog/<username>/', methods=["GET"])
def get_chatlog(username):
	return jsonify(chat.get_chatlog_from_room(username))

@app.route('/chatroom/rooms/', methods=["GET"])
def get_rooms():
	return jsonify(chat.get_rooms_as_list())

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
	chat.create_room('General')

	app.run()
	#app.run(debug=True)		
