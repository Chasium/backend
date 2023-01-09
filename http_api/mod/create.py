from apigen.generated.mod.create import CreateModRequest, CreateModResponse
from db import db
from db.models.mod import ModData
from http_api.auth.util import get_user


def create(req: CreateModRequest):
    res = CreateModResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res

    card = user.cards.filter_by(name=req.name).first()
    if card is not None:
        res.solve__code(3)
        return res

    card = ModData(req.name, req.content, user)
    db.session.add(card)
    db.session.commit()
    res.solve__code(0)
    return res
