from apigen.generated.user.get_my_id import getIdRequest, getIdResponse
from http_api.auth.util import get_user
from db.models.user import UserData

def getMyId(req: getIdRequest):
    res = getIdResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    res.solve__code(0)
    res.solve__id(user.getName())
    return res