from datetime import datetime

import jwt
from bson import ObjectId
from flask import request
from pymongo.errors import DuplicateKeyError

from src.models.mongo.conversation import Conversation
from src.models.mongo.mark_conversation import MarkConversation
from src.models.mongo.user import User
from src.models.mongo.user_conversation import UserConversation
from src.utils import auth
from src.utils.auth import decode_token


class ConversationController:
    def list_conversations(self):
        try:
            conversations_data = list()
            limit = 100
            user_id = decode_token('user_id')

            user_conversations = UserConversation().list_conversation_id(user_id = ObjectId(user_id), limit = limit)

            for user_conversation in user_conversations:
                conversation_id = str(user_conversation.get('conversation_id'))
                conversation = Conversation().get_conversation(conversation_id=ObjectId(conversation_id))
                if conversation:
                    response_conversation = dict()
                    response_conversation['_id'] = str(conversation['_id'])
                    last_time = user_conversation.get('last_message_time')
                    if last_time:
                        response_conversation['last_message_time'] = last_time.strftime('%d/%m/%Y %H:%M:%S')
                    participants = conversation.get('participants', [])
                    for participant in participants:
                        if 'user_id' in participant and participant['user_id'] != user_id:
                            response_conversation['recipient_id'] = str(participant['user_id'])
                            response_conversation['recipient_name'] = str(participant['username'])
                    if conversation['snippet']:
                        response_conversation['snippet'] = conversation['snippet']
                    conversations_data.append(response_conversation)

            if not conversations_data:
                return{
                    'code': 200,
                    'message': 'Không có cuộc hội thoại nào!',
                    'data': conversations_data
                }, 200

            return{
                'code': 200,
                'data': conversations_data
            }

        except Exception as e:
            print(e)
            return{
                'code': 400,
                'message': str(e)
            }, 400

    def create_conversation(self):
        try:
            data = request.json
            user_id = decode_token('user_id')
            request_field = ['email']
            if not data['email']:
                return{
                    'code': 400,
                    'message': 'Vui lòng điền địa chỉ email để khởi tạo cuộc hội thoại'
                }, 400
            if not all(field in data for field in request_field):
                return {
                    'code': 400,
                    'message': 'Missing required fields'
                }, 400

            email = data['email'].strip()

            recipient_data = User().get_user(email=email)
            user_data = User().get_user(user_id = ObjectId(user_id))

            if not recipient_data.email:
                return{
                    'code': 400,
                    'message': 'Không có người dùng thỏa mãn email'
                }, 400

            if user_data.email == email:
                return{
                    'code': 400,
                    'message': 'Đây là địa chỉ email của bạn. Vui lòng nhập địa chỉ email khác!'
                }, 400

            recipient_id = str(recipient_data.id)
            recipient_name = recipient_data.username
            user_name = user_data.username

            array_mark = [recipient_id, user_id]
            array_mark.sort()
            mark_key = "-".join(array_mark)
            try:
                MarkConversation(mark_key = mark_key).create_mark_conversation()
            except DuplicateKeyError:
                return{
                    'code': 400,
                    'message': 'Hội thoại đã được tạo'
                }, 400

            participants = []
            if user_data:
                participant = dict()
                participant['username'] = user_name
                participant['user_id'] = user_id
                participants.append(participant)
            if recipient_data:
                participant = dict()
                participant['username'] = recipient_name
                participant['user_id'] = recipient_id
                participants.append(participant)

            conversation_data = Conversation(
                participants=participants,
                snippet=''
            ).save_conversation()
            response_conversation = dict()
            if conversation_data:
                response_conversation['_id'] = str(conversation_data['_id'])
                last_time = conversation_data.get('last_message_time')
                if last_time:
                    response_conversation['last_message_time'] = last_time.strftime('%d/%m/%Y %H:%M:%S')
                participants = conversation_data.get('participants', [])
                for participant in participants:
                    if 'user_id' in participant and participant['user_id'] != user_id:
                        response_conversation['recipient_id'] = str(participant['user_id'])
                        response_conversation['recipient_name'] = str(participant['username'])
                if conversation_data['snippet']:
                    response_conversation['snippet'] = conversation_data['snippet']
                for participant in participants:
                    UserConversation(
                        user_id=ObjectId(participant['user_id']),
                        conversation_id=ObjectId(conversation_data['_id']),
                        is_group='false',
                        is_reply='false'
                    ).save_user_conversation()

            return{
                'code': 200,
                'message': 'Tạo hội thoại thành công',
                'data': response_conversation
            }
        except DuplicateKeyError as e:
            error_message = str(e.details)
            index_name = None
            if 'index: ' in error_message:
                index_name = error_message.split('index:')[1].split(" ")[1]
            if index_name == "_id_1":
                return {
                    "code": 400,
                    "message": "Đã tồn tại cuộc hội thoại với email đã nhập"
                }, 400
            return{
                'code': 400,
                'message': str(e)
            }, 400