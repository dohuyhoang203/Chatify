from flask import Blueprint

from src.apis import ApiUrl, Method

ping_mod = Blueprint('ping', __name__)


@ping_mod.route(ApiUrl.ping, methods=[Method.GET])
def ping():
    return {
        'code': 200,
        'message': 'Success'
    }

