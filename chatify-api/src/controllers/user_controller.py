import re

from src.models import redis
from src.models.redis import BaseRedis
from src.utils import auth
import bcrypt
import jwt
from bson import ObjectId
from flask import request
from pymongo.errors import DuplicateKeyError

from src.models.mongo.user import User

class UserController:
    def list_users(self):
        users = User().list_users()
        response_users = list()
        for user in users:
            if '_id' in user:
                user['_id'] = str(user['_id'])
            if 'created_at' in user:
                user['created_at'] = user['created_at'].strftime('%d/%m/%Y %H:%M:%S')
            if 'updated_at' in user:
                user['updated_at'] = user['updated_at'].strftime('%d/%m/%Y %H:%M:%S')
            response_users.append(user)
        return {
            'code': 200,
            'data': response_users
        }

    def login(self):
        try:
            request_body = request.json
            request_field = ['email', 'password']
            if not all(field in request_body for field in request_field):
                return{
                    'code': 400,
                    'message': 'Missing required fields'
                }, 400
            if not request_body['email'] or not request_body['password']:
                return{
                    'code': 400,
                    'message': 'Hãy nhập đầy đủ email và mật khẩu!'
                }, 400
            email = request_body['email'].strip()
            password = request_body['password'].strip()
            user = User().get_user(email = email)
            if not user.email:
                return {
                    'code': 400,
                    'message': "Email chưa từng được đăng ký trước đó!"
                }, 400
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return{
                    'code': 400,
                    'message': "Mật khẩu không đúng. Vui lòng nhập lại!"
                }, 400

            token = jwt.encode({
                "user_id": str(user.id),
                "username": user.username
            }, auth.secret_key, algorithm='HS256')

            BaseRedis().set_data(key = token, value = token, ex = 1800)

            return{
                'code': 200,
                'message': "Đăng nhập thành công",
                'token': token,
                'data': user.deserialize()
            }
        except Exception as e:
            return {
                'code': 400,
                'message': str(e)
            }, 400

    def is_valid_email(self, email):
        return bool(re.match(r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email))

    def is_valid_password(self, password):
        return bool(re.match(r"^[a-zA-Z0-9_.]+$",password))

    def sign_up(self):
        try:
            request_body = request.json
            required_fields = ['username', 'email', 'password', 'confirm_password', 'phone_number']
            if not all(field in request_body for field in required_fields):
                return {
                    "code": 400,
                    "message": "Missing required fields"
                }, 400

            if not request_body['username'] or not request_body['email'] or not request_body['password'] or not request_body['confirm_password'] or not request_body['phone_number']:
                return{
                    "code": 400,
                    "message": "Hãy nhập đầy đủ các trường thông tin đăng ký!"
                }, 400

            username = request_body['username'].strip()
            email = request_body['email'].strip()
            password = request_body['password'].strip()
            confirm_password = request_body['confirm_password'].strip()
            phone_number = request_body['phone_number'].strip()

            if len(username) < 3:
                return {
                    "code": 400,
                    "message": "Tên đăng nhập phải có ít nhất 3 kí tự"
                }, 400

            if len(password) < 6:
                return {
                    "code": 400,
                    "message": "Mật khẩu phải chứa ít nhất 6 ký tự"
                }, 400
            if not self.is_valid_password(password):
                return {
                    'code': 400,
                    'message': 'Mật khẩu không được chứa ký tự đặc biêt!'
                }, 400
            if password != confirm_password:
                return {
                    "code": 400,
                    "message": "Mật khẩu xác nhận không đúng. Vui lòng nhập lại"
                }, 400

            if len(phone_number) < 10 or not phone_number.isdigit():
                return {
                    "code": 400,
                    "message": "Số điện thoại chỉ chứa chữ số!"
                }, 400

            if not self.is_valid_email(email):
                return {
                    'code': 400,
                    'message': 'Email không được chứa ký tự đặc biệt!'
                }, 400

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User(password=hashed_password.decode('utf-8'),
                 username=username,
                 email=email,
                 phone_number=phone_number,
                 status='Active',
                 avatar="http://avatar.com/1234").save_user()

            return {
                "code": 200,
                "message": "Sign up successful"
            }

        except DuplicateKeyError as e:
            error_message = str(e.details)
            index_name = None
            if 'index: ' in error_message:
                index_name = error_message.split('index:')[1].split(" ")[1]
            if index_name == "email_1":
                return {
                    "code": 400,
                    "message": "Email đã được đăng ký trước đó"
                }, 400
            elif index_name == "username_1":
                return {
                    "code": 400,
                    "message": "Tên đăng nhập đã được sử dụng trước đó"
                }, 400
            return{
                "code": 400,
                "message": error_message
            }, 400

    def change_password(self):
        try:
            user_id = auth.decode_token('user_id')
            request_body = request.json
            required_fields = ['old_password', 'new_password', 'confirm_password']
            if not all(field in request_body for field in required_fields):
                return {
                    "code": 400,
                    "message": "Missing required fields"
                }, 400

            old_password = request_body['old_password'].strip()
            new_password = request_body['new_password'].strip()
            confirm_password = request_body['confirm_password'].strip()
            user = User().get_user(user_id = ObjectId(user_id))

            if not bcrypt.checkpw(old_password.encode('utf-8'), user['password'].encode('utf-8')):
                return {
                    'code': 400,
                    "message": "Mật khẩu không chính xác"
                }, 400
            if len(new_password) < 6:
                return {
                    "code": 400,
                    "message": "Mật khẩu mới cần ít nhất 6 ký tự"
                }, 400
            if not self.is_valid_password(new_password):
                return {
                    'code': 400,
                    'message': 'Mật khẩu mới không được chứa những ký tự đặc biệt'
                }, 400
            if confirm_password != new_password:
                return{
                    "code": 400,
                    "message": "Mật khẩu xác nhận không chính xác. Vui lòng nhập lại"
                }, 400

            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            User().update_user(user_id = ObjectId(user_id),password=hashed_password.decode('utf-8'))

            return{
                "code": 200,
                "message": "Đổi mật khẩu thành công"
            }
        except Exception as e:
            return {
                "code": 400,
                "message": str(e)
            }, 400

    def logout(self):
        try:
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            BaseRedis().del_data(token)
            return{
                'code': 200,
                'message': 'Bạn đã đăng xuất'
            }
        except Exception as e:
            return {
                "code": 400,
                "message": str(e)
            }, 400