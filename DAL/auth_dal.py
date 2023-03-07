import requests
from gevent import monkey
_ = monkey.patch_all()
from pymongo import MongoClient
from bson import ObjectId
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
import os
from dotenv import load_dotenv
load_dotenv()


class AuthDal:
    def __init__(self):
        self.__client = MongoClient(os.environ.get("MONGO_DB_URI"),connect=False)
        self.__db = self.__client["Chat-App"]
        self.__collection = self.__db["Users"]

    def register_user(self, username, password):
        self.__collection.insert_one(
            {"username": username, "password": password, "contacts": [], "groups": [], "profile_pic": "https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg"})
        new_user = self.__collection.find_one({"username": username})
        return new_user

    def login_user(self, username, password):
        user = self.__collection.find_one({"username": username})
        if user["password"] == password:
            return user
        else:
            return "username or password incorrect!"

    def __check_user(self, username, password):

        user = self.__collection.find_one({"username": username})
        if user and user["password"] == password:
            return str(user["_id"])
        else:
            return None

    def get_token(self, username, password):
        user_id = self.__check_user(username, password)
        token = None
        if user_id is not None:
            token = create_access_token(identity=user_id)

        return token

    def verify_token(self):

        user_id = get_jwt_identity()
        if user_id:
            return {"boolean": True, "id": user_id}
        else:
            return False
