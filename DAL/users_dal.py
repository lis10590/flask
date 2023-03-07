import requests
from gevent import monkey
_ = monkey.patch_all()
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()


class UsersDal:
    def __init__(self):
        self.__client = MongoClient(os.environ.get("MONGO_DB_URI"),connect=False)
        self.__db = self.__client["Chat-App"]
        self.__collection = self.__db["Users"]

    def get_all_users(self):
        users = list(self.__collection.find({}))
        return users

    def get_user(self, id):
        user = self.__collection.find_one({"_id": ObjectId(id)})
        return user

    def add_new_user(self, user):
        self.__collection.insert_one(
            {"username": user["username"], "password": user["password"], "rooms": [], "contacts": [], "blocked": [], "profile_pic": "https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg"})
        username = user["username"]
        rooms = user["rooms"]
        users = list(self.__collection.find({}))
        return {"users": users, "username": username, "rooms": rooms}

    def delete_user(self, username):
        user = self.__collection.find_one({"username": username})
        id = user["_id"]
        self.__collection.delete_one({"username": username})
        return id

    def update_rooms(self, user):
        self.__collection.update_one({"_id": ObjectId(user["id"])}, {
            "$push": {"rooms": user["room"]}})
        users = list(self.__collection.find({}))
        return users

    def update_profile_pic(self, user):
        self.__collection.update_one({"_id": ObjectId(user["id"])}, {
            "$push": {"profile_pic": user["profile_pic"]}})
        users = list(self.__collection.find({}))
        return users

    def add_to_blocked(self, user):
        self.__collection.update_one({"_id": ObjectId(
            user["id"]), "blocked.id": user["contactId"]}, {"$set": {"blocked.$.blocked": True}})
        users = list(self.__collection.find({}))
        return users

    def remove_from_blocked(self, user):
        self.__collection.update_one({"_id": ObjectId(user["id"]), "blocked.id": user["contactId"]},  {
                                     "$set": {"blocked.$.blocked": False}})
        users = list(self.__collection.find({}))
        return users

    def add_contact(self, user):
        contact = self.__collection.find_one({"username": user["contact"]})
        self.__collection.update_one({"_id": ObjectId(user["id"])}, {
            "$push": {"contacts": str(contact["_id"])}
        })

        obj = {}
        obj["id"] = str(contact["_id"])
        obj["blocked"] = False

        self.__collection.update_one({"_id": ObjectId(user["id"])}, {
            "$push": {"blocked": obj}
        })

        self.__collection.update_one({"_id": contact["_id"]}, {
            "$push": {"contacts": user["id"]}
        })

        obj2 = {}
        obj2["id"] = user["id"]
        obj2["blocked"] = False

        self.__collection.update_one({"_id": contact["_id"]}, {
            "$push": {"blocked": obj2}
        })

        users = list(self.__collection.find({}))
        return users

    def get_contacts(self, id):
        users = self.__collection.find_one({"_id": ObjectId(id)})
        return users["contacts"]

    def add_group(self, user):
        self.__collection.update_one({"_id": ObjectId(user["id"])}, {
            "$push": {"groups": user["group"]}
        })
        users = list(self.__collection.find({}))
        return users
