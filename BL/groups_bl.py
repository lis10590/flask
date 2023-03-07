from DAL.groups_dal import *
from DAL.users_dal import *


class GroupsBL:
    def __init__(self):
        self.__groups_dal = GroupsDal()
        self.__users_dal = UsersDal()

    def get_groups(self):
        groups = self.__groups_dal.get_all_groups()
        return groups

    def get_members_from_group(self, id):
        members_ids = self.__groups_dal.get_members_from_group(id)
        members = []
        for member_id in members_ids:
            member = self.__users_dal.get_user(member_id)
            print(member)
            members.append(member)

        return members

    def add_new_group(self, group):
        new_group = self.__groups_dal.add_new_group(group)
        return new_group

    def add_member_to_group(self, obj):
        groups = self.__groups_dal.add_member_to_group(obj)
        user = {}
        user["id"] = groups["new_member"]
        user["group"] = groups["group_id"]
        self.__users_dal.add_group(user)

        return groups

    def delete_group(self, id):
        id = self.__groups_dal.delete_group(id)
        return id
