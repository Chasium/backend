from apigen.generated.user.get_my_info import GetMyInfoRequest, GetMyInfoResponse
from http_api.auth.util import get_user
from db import db
from sqlalchemy import func
from db.models.userInfo import UserInfoData
from typing import List

def getMyInfo(req: GetMyInfoRequest):
    print('enter get my info')
    res = GetMyInfoResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    print("===================================================")
    info_list: List[UserInfoData]  = user.user_info.order_by(UserInfoData.id.desc())
    print(info_list)
    print("count: ", info_list.count())
    print("===================================================")
    if info_list.count() == 0:  # 还没有上传过头像
        res.solve__code(2)
        return res
    res.solve__code(0)
    # getInfo: UserInfoData = user.user_info.order_by(UserInfoData.id.desc())[0]
    res.solve__img(info_list[0].img)
    return res
