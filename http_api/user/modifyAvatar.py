from apigen.generated.user.modifyAvatar import modifyAvatarRequest, modifyAvatarResponse
from http_api.auth.util import get_user
from db import db

def uploadImage(req: modifyAvatarRequest):
    res = modifyAvatarResponse()
    user = get_user(req.session)
    old_user = user
    if user is None:
        res.solve__code(1)
        return res
    user.modifyImage(req.img)
    print('Got img: ', req.img, 'type: ', type(req.img))
    db.session.delete(old_user)
    db.session.add(user)
    db.session.commit()
    res.solve__code(0)
    return res
