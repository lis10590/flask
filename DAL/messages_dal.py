from gevent import monkey
_ = monkey.patch_all()
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()


class MessagesDal:
    def __init__(self):
        self.__client = MongoClient(os.environ.get("MONGO_DB_URI"),connect=False)
        self.__db = self.__client["Chat-App"]
        self.__collection = self.__db["Messages"]

    def get_all_messages(self):
        messages = list(self.__collection.find({}))
        return messages

    def get_all_messages_by_username(self, username):
        messages = list(self.__collection.find({"username": username}))
        return messages

    def add_message(self, obj):
        self.__collection.insert_one(
            {"author": obj["author"], "message": obj["message"], "date": obj["date"], "destination": obj["destination"]})

        messages = list(self.__collection.find({}))
        return messages
