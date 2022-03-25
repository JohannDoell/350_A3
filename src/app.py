import json
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, AnyDict
from spyne.protocol.json import JsonDocument
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import rooms

# === Classes ===

# === Global Variables ===

chat = rooms.Rooms()


# === Routes ===

# == Post ==

class CorsService(ServiceBase):
    origin = '*'


def _on_method_return_object(ctx):
    ctx.transport.resp_headers['Access-Control-Allow-Origin'] = \
        ctx.descriptor.service_class.origin


CorsService.event_manager.add_listener('method_return_object',
                                       _on_method_return_object)


class ChatroomService(CorsService):
    @rpc(Unicode, _returns=Unicode)
    def register_user(self, username):
        response = "Server received: " + username
        print(response)

        chat.add_user(username)

        yield response

    @rpc(Unicode, Unicode, _returns=Unicode)
    def receive_message(self, username, message):
        response = "Server received: " + username + " " + message
        print(response)

        # Commands
        if message[0] == '/':
            print("Command received.")
            command_to_give = str(message[1:])
            print(command_to_give)
            command_to_give = command_to_give.split()
            chat.parse_command(command_to_give[0], command_to_give[1:], username)
        else:
            user_room = chat.get_user_room(username)
            chat.add_message_to_room(user_room, username, message)
        yield response

    # == Get ==

    @rpc(Unicode, _returns=AnyDict)
    def get_chatlog(self, username):
        print("Received get request for log for user: " + username)
        return chat.get_chatlog_from_room(username)

    @rpc(_returns=AnyDict)
    def get_rooms(self):
        print("Received get request for rooms")
        return chat.get_rooms_as_list()


# == Flask Helpers ==

# @app.after_request
# def add_headers(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     return response


# === Utility ===

# def convert_json_to_dict(json_to_convert):
#     json_as_str = json.dumps(json_to_convert)
#     json_as_dict = json.loads(json_as_str)
#     return json_as_dict


# === Main ===

application = Application([ChatroomService], 'chatroom',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=JsonDocument())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
