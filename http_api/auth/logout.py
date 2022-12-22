from apigen.generated.auth.logout import LogoutRequest, LogoutResponse

from http_api.auth.util import login_user


def logout(req: LogoutRequest):
    res = LogoutResponse()
    res.solve__code(-1)

    print('logout session', req.session)
    if login_user.get(req.session):
        login_user.pop(req.session)
        res.solve__code(0)
    return res