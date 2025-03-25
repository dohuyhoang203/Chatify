import datetime

from src.common.constants import Common
from src.models.mongo import BaseMongo


class User(BaseMongo):
    id = ''
    username = ''
    email = ''
    password = ''
    phone_number = ''
    avatar = ''
    status = ''
    created_at = ''
    updated_at = ''

    def __init__(self, **kwargs):
        super().__init__()
        self.collection_name = 'users'
        self.id = kwargs.get('_id')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.phone_number = kwargs.get('phone_number')
        self.avatar = kwargs.get('avatar')
        self.status = kwargs.get('status')
        created_at = kwargs.get('created_at')
        if created_at:
            created_at = created_at.strftime(Common.DATE_TIME_FORMAT)
        self.created_at = created_at
        updated_at = kwargs.get('updated_at')
        if updated_at:
            updated_at = updated_at.strftime(Common.DATE_TIME_FORMAT)
        self.updated_at = updated_at

    def deserialize(self):
        return {
            "_id": str(self.id),
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "avatar": self.avatar,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def list_users(self, username = None, email = None):
        filter_option = dict()
        if username:
            filter_option['username'] = username
        if email:
            filter_option['email'] = email
        return self.find(filter_option).sort('updated_at', -1)

    def get_user(self, email = None, username = None, user_id = None, password = None):
        user = dict()
        try:
            filter_option = dict()
            if username:
                filter_option['username'] = username
            if email:
                filter_option['email'] = email
            if user_id:
                filter_option['_id'] = user_id
            if password:
                filter_option['password'] = password
            result = self.find_one(filter_option)
            if result:
                user = result
        except Exception as e:
            print(f'get_user Error: {str(e)}')
        return User(**user)

    def save_user(self):
        new_user = dict()
        new_user['username'] = self.username
        new_user['email'] = self.email
        new_user['phone_number'] = self.phone_number
        new_user['password'] = self.password
        new_user['avatar'] = self.avatar
        new_user['status'] = self.status
        new_user['created_at'] = datetime.datetime.now(datetime.UTC)
        new_user['updated_at'] = datetime.datetime.now(datetime.UTC)
        self.insert_one(new_user)
        if '_id' in new_user:
            new_user['_id'] = str(new_user['_id'])
        return new_user

    def update_user(self, user_id = None, password = None):
        filter_option = dict()
        if password:
            filter_option['password'] = password
        filter_option['updated_at'] = datetime.datetime.now(datetime.UTC)
        results = self.update_one(user_id, filter_option)
        return results.modified_count > 0