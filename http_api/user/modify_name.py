from apigen.generated.user.modify_name import modifyNameRequest, modifyNameResponse
from http_api.auth.util import get_user
from db import db


def modifyName(req: modifyNameRequest):
    res = modifyNameResponse()
    user = get_user(req.session)
    old_user = user
    if user is None:
        res.solve__code(1)
        return res
    user.modifyNickname(req.new_name)
    print('Got newName: ', req.new_name)
    db.session.delete(old_user)
    db.session.add(user)
    db.session.commit()
    res.solve__code(0)
    return res