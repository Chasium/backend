from apigen.generated.auth.login import LoginRequest, LoginResponse

from http_api.auth.util import user_exists, password_verified, logged_in, user_login, get_session_by_name


def login(req: LoginRequest):
    res = LoginResponse()
    res.solve__code(404)
    error = None

    print('User,', req.user_name, req.password)

    if not user_exists(req.user_name):
        error = 'user not found'
        res.solve__code(1)
    elif not password_verified(req.user_name, req.password):
        error = 'wrong password'
        res.solve__code(2)
    elif logged_in(req.user_name):
        error = 'login already'
        res.solve__code(3)
        res.solve__session(get_session_by_name(req.user_name))

    if error is None or error == 'login already':
        print('Verified')
        temp_session = user_login(req.user_name)
        res.solve__code(0)
        res.solve__session(temp_session)
    else:
        print(error)
    return res
