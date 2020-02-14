from server import app
from flask_api import status
from flask import render_template, jsonify, request
from server.forms import position_form
from model import gameroom, rooms, user, optionlist, job
from datetime import datetime, timedelta
from server.helpers import room_not_found, invalid_token, access_denied, user_exists, validate_game, room_exists, validate_user
import jwt
import random

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html"), status.HTTP_200_OK

@app.route('/room/<room_name>/create', methods=['POST'])
def create_room():
	
	new_room = chatroom(room_name)
	room_id = new_room.get_id()
	rooms.get_map().update({room_id: new_room})

	# Expire in five hours
	expiry = datetime.utcnow() + timedelta(hours=5)
	room_token = jwt.encode({"role": "room", "exp": expiry}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf8')
	
	res = {
		"room_id": room_id
		"token": room_token
	}
	
	return jsonify(res), status.HTTP_201_CREATED
