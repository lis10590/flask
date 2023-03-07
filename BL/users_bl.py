from DAL.users_dal import *
from DAL.groups_dal import *


class UsersBL:
    def __init__(self):
        self.__users_dal = UsersDal()
        self.__groups_dal = GroupsDal()

    def get_users(self):
        users = self.__users_dal.get_all_users()
        return users

    def add_new_user(self, user):
        new_user = self.__users_dal.add_new_user(user)
        return new_user

    def delete_user(self, username):
        id = self.__users_dal.delete_user(username)
        return id

    def update_rooms(self, user):
        users = self.__users_dal.update_rooms(user)
        return users

    def update_profile_pic(self, user):
        users = self.__users_dal.update_profile_pic(user)
        return users

    def add_blocked(self, user):
        users = self.__users_dal.add_to_blocked(user)
        return users

    def remove_blocked(self, user):
        users = self.__users_dal.remove_from_blocked(user)
        return users

    def add_new_contact(self, user):
        users = self.__users_dal.add_contact(user)
        return users

    def get_all_contacts(self, id):
        users = self.__users_dal.get_contacts(id)
        return users

    def add_group_to_user(self, obj):
        groups = self.__groups_dal.add_new_group(obj)
        for group in groups:
            if group["name"] == obj["name"]:
                id = str(group["_id"])
        user = {}
        user["group"] = id
        user["id"] = obj["userId"]

        users = self.__users_dal.add_group(user)
        return users
