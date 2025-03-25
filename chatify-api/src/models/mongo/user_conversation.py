import datetime
from src.common.constants import Common
from src.models.mongo import BaseMongo


class UserConversation(BaseMongo):
    conversation_id = ''
    user_id = ''
    is_read = False
    is_reply = False
    last_message_time = ''

    def __init__(self, **kwargs):
        super().__init__()
        self.collection_name = 'user_conversation'
        self.conversation_id = kwargs.get('conversation_id')
        self.user_id = kwargs.get('user_id')
        self.is_read = kwargs.get('is_read', False)
        self.is_reply = kwargs.get('is_reply', False)
        last_message_time = kwargs.get('last_message_time')
        if last_message_time:
            last_message_time = last_message_time.strftime(Common.DATE_TIME_FORMAT)
        self.last_message_time = last_message_time

    def list_conversation_id(self, user_id = None, last_message_time = None, last_id = None, limit = 10):
        filter_option = dict()
        if user_id:
            filter_option['user_id'] = user_id
        if last_message_time and last_id:
            filter_option['$or'] = [
                {'last_message_time': {'$lt': last_message_time}},
                {'last_message_time': last_message_time, '_id': {'$lt': last_id}}
            ]
        return self.find(filter_option).sort([('last_message_time', -1), ('_id', -1)]).limit(limit)

    def save_user_conversation(self):
        new_user_conversation = dict()
        new_user_conversation['user_id'] = self.user_id
        new_user_conversation['conversation_id'] = self.conversation_id
        new_user_conversation['is_read'] = self.is_read
        new_user_conversation['is_reply'] = self.is_reply
        new_user_conversation['last_message_time'] = datetime.datetime.now(datetime.UTC)
        self.insert_one(new_user_conversation)
        if 'user_id' in new_user_conversation:
            new_user_conversation['user_id'] = str(new_user_conversation['user_id'])
        if 'conversation_id' in new_user_conversation:
            new_user_conversation['conversation_id'] = str(new_user_conversation['conversation_id'])
        return new_user_conversation