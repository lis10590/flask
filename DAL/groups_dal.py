import requests
from gevent import monkey
_ = monkey.patch_all()
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()


class GroupsDal:
    def __init__(self):
        self.__client = MongoClient(os.environ.get("MONGO_DB_URI"),connect=False)
        self.__db = self.__client["Chat-App"]
        self.__collection = self.__db["Groups"]

    def get_all_groups(self):
        groups = list(self.__collection.find({}))
        return groups

    def get_members_from_group(self, id):
        group = self.__collection.find_one({"_id": ObjectId(id)})
        members = group["members"]
        return members

    def add_new_group(self, group):
        if len(group["members"]) == 0:
            self.__collection.insert_one(
                {"name": group["name"], "members": [], "profile_pic": "https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg"})
            groups = list(self.__collection.find({}))
            return groups
        else:
            self.__collection.insert_one(
                {"name": group["name"], "members": group["members"], "profile_pic": "https://deejayfarm.com/wp-content/uploads/2019/10/Profile-pic.jpg"})
            groups = list(self.__collection.find({}))
            return groups

    def add_member_to_group(self, obj):

        self.__collection.update_one({"_id": ObjectId(obj["id"])}, {
                                     "$push": {"members": obj["user"]}})
        group = self.__collection.find_one({"_id": ObjectId(obj["id"])})
        groups = list(self.__collection.find({}))
        return {"groups": groups, "group_members": group["members"], "group_id": obj["id"], "new_member": obj["user"]}

    def delete_group(self, id):
        self.__collection.delete_one({"_id": ObjectId(id)})
        return id
