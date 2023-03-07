from flask import Flask, jsonify
import json
from flask_cors import CORS
from bson import ObjectId
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room
from flask_socketio import send, emit
from routers.users_router import users
from routers.groups_router import groups
from routers.auth_router import auth
from routers.messages_router import messages
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
load_dotenv()


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
jwt = JWTManager(app)
CORS(app,origins=os.environ.get("ORIGIN"))
socketio = SocketIO(app, cors_allowed_origins=[os.environ.get("ORIGIN")])


app.json_encoder = JSONEncoder


@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('client disconnected')


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    # send(username + 'has entered the room.')
    print(username + " entered room " + room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(username + ' has left the room ' + room)
    send(username + ' has left the room.', to=room)


@socketio.on('message')
def handle_message(data):
    room = data["room"]
    # join_room(room)
    emit("message", data,  to=room)
    print(data)


# app.run()
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(groups, url_prefix="/groups")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(messages, url_prefix="/messages")

# socketio.run(app)
