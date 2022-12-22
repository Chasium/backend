from apigen.generated.room.card import EditCardRequest, EditCardResponse, ExecScriptRequest, ExecScriptResponse
from apigen.generated.script.exec import EditCardEvent, ExecScriptEvent
from typing import Union
from http_api.auth.util import get_user
from ws_api.script.util import fake_frontend_session


def handle_edit_card(req: EditCardRequest):
    user = get_user(req.session)
    if user is None:
        res = EditCardResponse()
        res.solve__code(1)
        res.emit_back()

    event = EditCardEvent()
    event.solve__user(user.name)
    event.solve__property_id(req.property_id)
    event.solve__new_value(req.new_value)
    event.emit_to_room(fake_frontend_session)


def handle_exec_script(req: ExecScriptRequest):
    user = get_user(req.session)
    if user is None:
        res = ExecScriptResponse()
        res.solve__code(1)
        res.emit_back()

    event = ExecScriptEvent()
    event.solve__user(user.name)
    event.solve__script_id(req.script_id)
    event.emit_to_room(fake_frontend_session)


def card(req: Union[EditCardRequest, ExecScriptRequest]):
    if isinstance(req, EditCardRequest):
        handle_edit_card(req)
    else:
        handle_exec_script(req)
