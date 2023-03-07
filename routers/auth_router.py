from flask import Blueprint, jsonify, request, make_response
from BL.auth_bl import AuthBL
from flask_cors import cross_origin

auth = Blueprint('auth', __name__)

auth_bl = AuthBL()


@auth.route("/register", methods=['POST'])
@cross_origin()
def register():
    username = request.json["username"]
    password = request.json["password"]
    user = auth_bl.register_user(username, password)

    token = auth_bl.get_token(username, password)
    if token is not None:
        return make_response({"token": token, "user": user}, 200)
    else:
        return make_response({"error": "You're not authorized"}, 401)


@auth.route("/login", methods=['POST'])
@cross_origin()
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = auth_bl.login_user(username, password)
    if user == "username or password incorrect!":
        return jsonify(user)
    else:

        token = auth_bl.get_token(username, password)
        if token is not None:
            return make_response({"token": token, "user": user}, 200)
        else:
            return make_response({"error": "You're not authorized"}, 401)
