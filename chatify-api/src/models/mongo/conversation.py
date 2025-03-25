import datetime
from src.common.constants import Common
from src.models.mongo import BaseMongo

class Conversation(BaseMongo):
    _id = ''
    title = ''
    is_group = False
    participants = ''
    snippet = ''
    last_message_time = ''

    def __init__(self, **kwargs):
        super().__init__()
        self.collection_name = 'conversations'
        self.title = kwargs.get('title')
        self.participants = kwargs.get('participants')
        self.is_group = kwargs.get('is_group')
        self.snippet = kwargs.get('snippet')
        last_message_time = kwargs.get('last_message_time')
        if last_message_time:
            last_message_time = last_message_time.strptime(Common.DATE_TIME_FORMAT)
        self.last_message_time = last_message_time

    def get_conversation(self, conversation_id = None):
        filter_options = dict()
        if conversation_id:
            filter_options['_id'] = conversation_id
        return self.find_one(filter_options)

    def save_conversation(self):
        new_conversation = dict()
        new_conversation['title'] = self.title
        new_conversation['is_group'] = self.is_group
        new_conversation['participants'] = self.participants
        new_conversation['snippet'] = self.snippet
        new_conversation['last_message_time'] = datetime.datetime.now(datetime.UTC)
        self.insert_one(new_conversation)
        for participant in self.participants:
            if 'user_id' in participant:
                participant['user_id'] = str(participant['user_id'])
        if '_id' in new_conversation:
            new_conversation['_id'] = str(new_conversation['_id'])
        return new_conversation

