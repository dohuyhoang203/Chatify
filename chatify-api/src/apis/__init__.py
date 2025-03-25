class ApiUrl:
    ping = '/ping'

    list_user = '/user/list'
    sign_up = '/user/sign-up'
    find_user = '/user/find-user'
    login_user = '/user/login'
    change_password = '/user/change-password'
    logout_user = '/user/logout'

    list_conversation = '/conversation/list'
    create_conversation = '/conversation/create'

    list_message = '/message/list'
    send_message = '/message/send'

class Method:
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'
