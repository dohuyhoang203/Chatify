
from functools import wraps

import jwt
from flask import request, json

from src.models.redis import BaseRedis

secret_key = "secret_key"

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return {
                "code": 401,
                'message': 'Unauthorized',
            }, 401
        try:
            token_redis = BaseRedis().get_data(token)
            if not token_redis:
                return{
                    "code": 401,
                    'message': 'Token is expired',
                }, 401
            jwt.decode(token, secret_key, algorithms=['HS256'])
        except Exception as e:
            print(f'check_token Error: {str(e)}')
            return {
                "code": 401,
                'message': 'Unauthorized',
            }, 401
        return f(*args, **kwargs)
    return decorated

def decode_token(key):
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    data = jwt.decode(token, secret_key, algorithms=['HS256'])
    return data.get(key)
