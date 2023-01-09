from apigen.generated.user.get_my_info import GetMyInfoRequest, GetMyInfoResponse
from http_api.auth.util import get_user

def getMyInfo(req: GetMyInfoRequest):
    print('enter get my info')
    res = GetMyInfoResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    if user.img == "":  # 还没有上传过头像
        res.solve__code(2)
        return res
    res.solve__code(0)
    res.solve__img(user.img)
    return res
