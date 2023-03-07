from flask import Blueprint, jsonify, request
from BL.messages_bl import MessagesBL
from flask_cors import cross_origin

messages = Blueprint('messages', __name__)

messages_bl = MessagesBL()


@messages.route("/getMessages", methods=['GET'])
@cross_origin()
def get_all_messages():
    messages = messages_bl.get_messages()
    return jsonify(messages)


@messages.route("/getMessagesByUsername", methods=['GET'])
@cross_origin()
def get_all_messages_by_username():
    username = request.json
    print(username)
    messages = messages_bl.get_messages_by_username(username)
    return jsonify(messages)


@messages.route("/addMessage", methods=['PUT'])
@cross_origin()
def get_messages_by_username():
    obj = request.json
    messages = messages_bl.add_message(obj)
    return jsonify(messages)
