from flask import Blueprint

from src.apis import ApiUrl, Method
from src.controllers.message_controller import MessageController

message_mod = Blueprint('message', __name__)

@message_mod.route(ApiUrl.list_message, methods = [Method.GET])
def list_message():
    return MessageController().list_messages()

@message_mod.route(ApiUrl.send_message, methods = [Method.POST])
def send_message():
    return MessageController().send_message()