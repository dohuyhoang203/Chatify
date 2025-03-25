from flask import Blueprint

from src.apis import ApiUrl, Method
from src.controllers.conversation_controller import ConversationController
from src.utils.auth import check_token

conversation_mod = Blueprint('conversation', __name__)

@conversation_mod.route(ApiUrl.list_conversation, methods=[Method.GET])
@check_token
def list_conversations():
    return ConversationController().list_conversations()

@conversation_mod.route(ApiUrl.create_conversation, methods=[Method.POST])
@check_token
def create_conversation():
    return ConversationController().create_conversation()