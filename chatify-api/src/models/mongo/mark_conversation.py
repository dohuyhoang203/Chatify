from src.models.mongo import BaseMongo


class MarkConversation(BaseMongo):
    _id = ''
    mark_key = ''

    def __init__(self, **kwargs):
        super().__init__()
        self.collection_name = 'mark_conversation'
        self._id = kwargs.get('_id')
        self.mark_key = kwargs.get('mark_key')

    def create_mark_conversation(self):
        new_mark_conversation = dict()
        new_mark_conversation['mark_key'] = self.mark_key
        self.insert_one(new_mark_conversation)
