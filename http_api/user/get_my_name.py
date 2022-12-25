from apigen.generated.user.get_my_name import GetMyNameRequest, GetMyNameResponse
from http_api.auth.util import get_user

def getMyName(req: GetMyNameRequest):
    print('enter get my name')
    res = GetMyNameResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    res.solve__code(0)
    res.solve__name(user.nickname)
    return res
