from apigen.generated.script.exec import EditCardResult, ExecScriptResult
from apigen.generated.room.card import EditCardResponse, ExecScriptResponse
from typing import Union
from ws_api.room.util import get_room


def exec(req: Union[EditCardResult, ExecScriptResult]):
    res: Union[EditCardResponse, ExecScriptResponse] = None
    if isinstance(req, EditCardResult):
        res = EditCardResponse()
    else:
        res = ExecScriptResponse()

    res.solve__code(req.code)

    if req.code == 0:
        room = get_room(req.room_id)
        room.player_card_map[req.user] = req.card
        res.solve__card(req.card)
    res.emit_to_room(req.room_id)
