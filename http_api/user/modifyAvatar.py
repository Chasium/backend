from apigen.generated.user.modifyAvatar import modifyAvatarRequest, modifyAvatarResponse
from http_api.auth.util import get_user
from db import db
from db.models.userInfo import UserInfoData
from typing import List

def uploadImage(req: modifyAvatarRequest):
    res = modifyAvatarResponse()
    user = get_user(req.session)
    print('Got img: ', req.img, 'type: ', type(req.img))
    if user is None:
        res.solve__code(1)
        return res
    userInfo = UserInfoData(req.img, user)
    db.session.add(userInfo)
    db.session.commit()
    # TODO 如果不是第一张，找到该user的上一张头像并删除
    info_list: List[UserInfoData]  = user.user_info.order_by(UserInfoData.id.desc())
    print(info_list)
    print("count: ", info_list.count())
    print("=======this count=========:\n",  info_list.count())
    if info_list.count() != 1:
        deleteInfo = info_list[1]
        db.session.delete(deleteInfo)
    res.solve__code(0)
    return res
