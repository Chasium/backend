from apigen.generated.card.create import CreateCardRequest, CreateCardResponse
from db import db
from db.models.card import CardData
from http_api.auth.util import get_user
from http_api.card_template.util import get_template


def create(req: CreateCardRequest):
    res = CreateCardResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res
    template = get_template(req.template_id)
    if template is None:
        res.solve__code(2)
        return res
    card = user.cards.filter_by(name=req.name).first()
    if card is not None:
        res.solve__code(3)
        return res
    card = CardData(req.name, req.card, user, template)
    db.session.add(card)
    db.session.commit()
    res.solve__code(0)
    return res
