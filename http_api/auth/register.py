from apigen.generated.auth.register import RegisterRequest, RegisterResponse

from http_api.auth.util import username_legal, password_legal, user_exists, add_user


def register(req: RegisterRequest):
    res = RegisterResponse()
    res.solve__code(404)
    error = None

    print('User,', req.user_name, req.password)

    if not username_legal(req.user_name):
        error = 'invalid username'
        res.solve__code(10)
    elif not password_legal(req.password):
        error = 'invalid password'
        res.solve__code(20)
    elif user_exists(req.user_name):
        error = 'user existed'
        res.solve__code(11)
    if error is None:
        add_user(req.user_name, req.password)
        res.solve__code(0)
    else:
        print(error)

    return res
