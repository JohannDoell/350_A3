from flask import Flask, request, jsonify

app = Flask(__name__)

testList = ["Apple", "Banana", "Orange"]

@app.route('/api/', methods=["POST"])
def main_interface():
    response = request.get_json()
    print(response)
    return jsonify(response)
    
@app.route('/user/setuser/', methods=["POST"])
def set_user():
	response = request.get_json()
	print(response)
	return jsonify(response)

@app.route('/rooms/<room>/chatlog/', methods=["GET"])
def get_chatlog(room):
	return jsonify(testList)
	#return room + " Chatlog"

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response
    
if __name__ == '__main__':
    app.run(debug=True)
