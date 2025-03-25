from flask import Blueprint

from src.apis import ApiUrl, Method
from src.controllers.user_controller import UserController
from src.utils.auth import check_token

user_mod = Blueprint('user', __name__)


@user_mod.route(ApiUrl.list_user, methods=[Method.GET])
@check_token
def list_user():
    return UserController().list_users()

@user_mod.route(ApiUrl.sign_up, methods=[Method.POST])
def sign_up():
    return UserController().sign_up()

@user_mod.route(ApiUrl.login_user, methods=[Method.POST])
def login():
    return UserController().login()

@user_mod.route(ApiUrl.change_password, methods=[Method.PUT])
@check_token
def change_password():
    return UserController().change_password()

@user_mod.route(ApiUrl.logout_user, methods=[Method.POST])
@check_token
def logout():
    return UserController().logout()