from typing import List
from apigen.generated.card.get_mine import GetMyCardsRequest, GetMyCardsResponse, Card
from db.models.card import CardData
from http_api.auth.util import get_user


def get_mine(req: GetMyCardsRequest):
    res = GetMyCardsResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res

    card_data_list: List[CardData] = user.cards.order_by(CardData.id.desc()).paginate(
        page=req.page, per_page=req.page_size, error_out=False).items

    cards: List[Card] = []
    for i in card_data_list:
        card = Card()
        card.solve__id(i.id)
        card.solve__name(i.name)
        card.solve__value(i.value)
        card.solve__template_id(i.template_id)
        cards.append(card)

    all_cards = user.cards.count()

    res.solve__cards(cards)
    res.solve__pages(all_cards // req.page_size +
                     bool(all_cards % req.page_size))
    res.solve__code(0)
    return res
