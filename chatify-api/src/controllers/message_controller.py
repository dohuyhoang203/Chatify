from datetime import datetime

import jwt
from bson import ObjectId
from flask import request

from src.models.mongo.message import Message
from src.utils import auth
from src.utils.auth import decode_token


class MessageController:
    def list_messages(self):
        try:
            conversation_id = request.args.get('conversation_id')
            limit = 100
            if not ObjectId.is_valid(conversation_id):
                return {
                    'code': 400,
                    'message': 'Invalid conversation ID'
                }, 400

            messages = Message().list_messages(conversation_id=ObjectId(conversation_id), limit=limit)
            response_messages = list()

            if messages:
                for message in messages:
                    if '_id' in message:
                        message['_id'] = str(message['_id'])
                    if 'conversation_id' in message:
                        message['conversation_id'] = str(message['conversation_id'])
                    if 'sender_id' in message:
                        message['sender_id'] = str(message['sender_id'])
                    if 'send_time' in message:
                        message['send_time'] = message['send_time'].strftime('%d-%m-%Y %H:%M:%S')
                    if 'attachments' in message:
                        attachments = message.get('attachments', [])
                        for attachment in attachments:
                            if 'url' in attachment:
                                attachment['url'] = str(attachment['url'])
                            if 'type' in attachment:
                                attachment['type'] = str(attachment['type'])
                            if 'title' in attachment:
                                attachment['title'] = str(attachment['title'])
                    response_messages.append(message)

            return {
                'code': 200,
                'data': response_messages
            }

        except Exception as e:
            return {
                'code': 400,
                'message': str(e)
            }, 400

    def send_message(self):
        try:
            data = request.json
            conversation_id = data.get('conversation_id')
            sender_id = decode_token('user_id')
            content = data.get('content')
            attachments = data.get('attachments', [])

            if not conversation_id or not ObjectId.is_valid(conversation_id):
                return {
                    'code': 400,
                    'message': 'Invalid or missing conversation ID'
                }, 400
            if not sender_id or not ObjectId.is_valid(sender_id):
                return {
                    'code': 400,
                    'message': 'Invalid or missing sender ID'
                }, 400
            if not content or not isinstance(content, str):
                return {
                    'code': 400,
                    'message': 'Content is required and must be a string'
                }, 400

            formatted_attachments = []
            for attachment in attachments:
                if not isinstance(attachment, dict):
                    continue
                formatted_attachment = {
                    'url': str(attachment.get('url', '')),
                    'type': str(attachment.get('type', '')),
                    'title': str(attachment.get('title', ''))
                }
                formatted_attachments.append(formatted_attachment)

            Message(
                conversation_id = ObjectId(conversation_id),
                sender_id = ObjectId(sender_id),
                content = content,
                attachments = formatted_attachments
            ).save_message()

            return {
                'code': 200,
                'message': 'Gửi tin nhắn thành công'
            }

        except Exception as e:
            return {
                'code': 400,
                'message': str(e)
            }, 400
