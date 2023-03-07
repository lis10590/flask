from DAL.messages_dal import *


class MessagesBL:
    def __init__(self):
        self.__messages_dal = MessagesDal()

    def get_messages(self):
        messages = self.__messages_dal.get_all_messages()
        return messages

    def get_messages_by_username(self, username):
        messages = self.__messages_dal.get_all_messages_by_username(username)
        return messages

    def add_message(self, obj):
        messages = self.__messages_dal.add_message(obj)
        return messages
