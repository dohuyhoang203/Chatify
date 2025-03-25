import datetime

import pymongo
from bson import ObjectId

from src.common.constants import Common
from src.models.mongo import BaseMongo


class Message(BaseMongo):
    _id = ''
    conversation_id = ''
    sender_id = ''
    content = ''
    attachment = ''
    send_time = ''

    def __init__(self, **kwargs):
        super().__init__()
        self.collection_name = 'messages'
        self.conversation_id = kwargs.get('conversation_id')
        self.sender_id = kwargs.get('sender_id')
        self.content = kwargs.get('content')
        self.attachment = kwargs.get('attachment')
        send_time = kwargs.get('send_time')
        if send_time:
            send_time = send_time.strftime(Common.DATE_TIME_FORMAT)
        self.send_time = send_time

    def list_messages(self, conversation_id = None, last_send_time = None, last_message_id = None, limit = 7):
        filter_option = dict()
        if conversation_id:
            filter_option['conversation_id'] = conversation_id
        if last_send_time and last_message_id:
            filter_option['$or'] = [
                {'send_time': {'$lt': last_send_time}},
                {'send_time': last_send_time, '_id': {'$lt': last_message_id}}
            ]
        return self.find(filter_option).sort([('send_time', 1), ('_id', -1)]).limit(limit)

    def get_message(self, conversation_id = None):
        filter_option = dict()
        if conversation_id:
            filter_option['conversation_id'] = conversation_id
        return self.find_one(filter_option)

    def save_message(self):
        new_message = dict()
        new_message['conversation_id'] = self.conversation_id
        new_message['sender_id'] = self.sender_id
        new_message['content'] = self.content
        new_message['attachment'] = self.attachment
        new_message['send_time'] = datetime.datetime.now(datetime.UTC)
        self.insert_one(new_message)
        if '_id' in new_message:
            new_message['_id'] = str(new_message['_id'])
        if 'conversation_id' in new_message:
            new_message['conversation_id'] = str(new_message['conversation_id'])
        if 'sender_id' in new_message:
            new_message['sender_id'] = str(new_message['sender_id'])
        return new_message