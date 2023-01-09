from apigen.generated.card.delete import DeleteCardRequest, DeleteCardResponse
from db import db
from http_api.auth.util import get_user


def delete(req: DeleteCardRequest):
    res = DeleteCardResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res

    card = user.cards.filter_by(id=req.id).first()
    if card is None:
        res.solve__code(2)
        return res

    db.session.delete(card)
    res.solve__code(0)
    return res
