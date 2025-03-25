from app import app
from src.apis.conversation import conversation_mod
from src.apis.message import message_mod
from src.apis.ping import ping_mod
from src.apis.user import user_mod

web_url_prefix = '/chatify/api'

app.register_blueprint(ping_mod, name='ping', url_prefix=web_url_prefix)
app.register_blueprint(user_mod, name='user', url_prefix=web_url_prefix)
app.register_blueprint(conversation_mod, name='conversation', url_prefix=web_url_prefix)
app.register_blueprint(message_mod, name='message', url_prefix=web_url_prefix)