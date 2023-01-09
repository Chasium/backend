from apigen.generated.room.game import SetCardRequest, SetCardResponse, SetTemplateRequest, SetTemplateResponse, PrepareRequest, PrepareResponse, StopPrepareRequest, StartGameResponse, StartGameRequest, StopPrepareResponse, EndGameRequest, EndGameResponse, CardTemplate, Card
from apigen.generated.script.init import InitGameEvent, CleanGameEvent
from typing import List, Union
from http_api.auth.util import get_user
from ws_api.room.util import get_user_room
from db.models.card_template import CardTemplateData
from db.models.card_script import CardScriptData
from db.models.card import CardData
from ws_api.script.util import fake_frontend_session
from db import db


def handle_set_template(req: SetTemplateRequest):
    res = SetTemplateResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res

    room = get_user_room(req.session)
    if room is None:
        res.solve__code(2)
        return res

    if room.host_name != user.name:
        res.solve__code(3)
        return res

    template: CardTemplateData = CardTemplateData.query.filter_by(
        id=req.template_id).first()
    if template is None:
        res.solve__code(4)
        return res

    room.template_id = template.id
    res.solve__code(0)

    res_template = CardTemplate()
    res_template.solve__id(template.id)
    res_template.solve__value(template.content)
    scripts: List[str] = []
    script_data_list: List[CardScriptData] = template.scripts.order_by(
        CardScriptData.in_card_id).all()
    for i in script_data_list:
        scripts.append(i.value)
    res_template.solve__scripts(scripts)
    res.solve__template(res_template)
    return res


def handle_set_card(req: SetCardRequest):
    res = SetCardResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return
    room = get_user_room(req.session)
    if room is None:
        res.solve__code(2)
        res.emit_back()
        return
    if room.host_name == user.name:
        res.solve__code(3)
        res.emit_back()
        return
    card: CardData = CardData.query.filter_by(id=req.card_id).first()
    if card is None or card.template_id != room.template_id:
        res.solve__code(3)
        res.emit_back()
        return

    room.player_card_map[user.name] = card.value
    room.player_card_id_map[user.name] = card.id
    res_card = Card()
    res_card.solve__id(card.id)
    res_card.solve__template_id(card.template_id)
    res_card.solve__value(card.value)
    res.solve__card(res_card)
    res.solve__code(0)
    res.solve__user(user.name)
    res.emit_to_room(room.id)


def handle_prepare(req: PrepareRequest):
    res = PrepareResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return
    room = get_user_room(req.session)
    if room is None:
        res.solve__code(2)
        res.emit_back()
        return
    if room.host_name == user.name or room.prepare_map[user.name] == True:
        res.solve__code(3)
        res.emit_back()
        return
    room.prepare_map[user.name] = True
    res.solve__code(0)
    res.solve__user(user.name)
    res.emit_to_room(room.id)
    return


def handle_stop_prepare(req: StopPrepareRequest):
    res = StopPrepareResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return
    room = get_user_room(req.session)
    if room is None:
        res.solve__code(2)
        res.emit_back()
        return
    if room.host_name == user.name or room.prepare_map[user.name] == False:
        res.solve__code(3)
        res.emit_back()
        return
    room.prepare_map[user.name] = False
    res.solve__code(0)
    res.solve__user(user.name)
    res.emit_to_room(room.id)
    return


def handle_start_game(req: StartGameRequest):
    res = StartGameResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return
    room = get_user_room(req.session)
    if room is None:
        res.solve__code(2)
        res.emit_back()
        return
    if user.name != room.host_name:
        res.solve__code(3)
        res.emit_back()
        return
    all_prepared = True
    for i in room.prepare_map:
        if not room.prepare_map[i]:
            all_prepared = False
    if not all_prepared:
        res.solve__code(3)
        res.emit_back()
        return

    event = InitGameEvent()
    event.solve__room_id(room.id)
    players: List[str] = []
    cards: List[str] = []
    for i in room.player_card_map:
        players.append(i)
        cards.append(room.player_card_map[i])
    event.solve__players(players)
    event.solve__cards(cards)
    template: CardTemplateData = CardTemplateData.query.filter_by(
        id=room.template_id).first()

    res_template = CardTemplate()
    res_template.solve__id(template.id)
    res_template.solve__value(template.content)
    scripts: List[str] = []
    script_data_list: List[CardScriptData] = template.scripts.order_by(
        CardScriptData.in_card_id).all()
    for i in script_data_list:
        scripts.append(i.value)
    res_template.solve__scripts(scripts)
    event.solve__template(res_template)
    event.emit_to_room(fake_frontend_session)
    res.solve__code(0)
    res.emit_to_room(room.id)
    return


def handle_end_game(req: EndGameRequest):
    res = EndGameResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return
    room = get_user_room(req.session)
    if room is None:
        res.solve__code(2)
        res.emit_back()
        return
    if user.name != room.host_name:
        res.solve__code(3)
        res.emit_back()
        return
    event = CleanGameEvent()
    event.solve__game_id(room.fake_frontend_id)
    event.emit_to_room(fake_frontend_session)

    for i in room.player_card_map:
        id = room.player_card_id_map[i]
        content = room.player_card_map[i]
        card: CardData = CardData.query.filter_by(id=id).first()
        card.value = content
        db.session.add(card)

    db.session.commit()
    res.solve__code(0)
    res.emit_to_room(room.id)
    return


def game(req: Union[SetTemplateRequest, SetCardRequest, PrepareRequest, StopPrepareRequest, StartGameRequest, EndGameRequest]):
    if isinstance(req, SetTemplateRequest):
        handle_set_template(req)
    if isinstance(req, SetCardRequest):
        handle_set_card(req)
    if isinstance(req, PrepareRequest):
        handle_prepare(req)
    if isinstance(req, StopPrepareRequest):
        handle_stop_prepare(req)
    if isinstance(req, StartGameRequest):
        handle_start_game(req)
    if isinstance(req, EndGameRequest):
        handle_end_game(req)
