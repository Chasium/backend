from apigen.generated.script.init import FakeFrontendConnectRequest, FakeFrontendConnectResponse, InitGameResult, CleanGameResult
from typing import Union
from ws_api.script.util import fake_frontend_session
from random import getrandbits
from ws_api.room.util import get_room
from flask_socketio import join_room


def handle_connect(req: FakeFrontendConnectRequest):
    global fake_frontend_session
    fake_frontend_session = hex(getrandbits(128))
    join_room(fake_frontend_session)
    res = FakeFrontendConnectResponse()
    res.solve__session(fake_frontend_session)
    res.emit_back()
    return res.to_json()


def handle_init(req: InitGameResult):
    room = get_room(req.room_id)
    room.fake_frontend_id = req.game_id
    return room


def handle_clean(req: CleanGameResult):
    pass


def init(req: Union[FakeFrontendConnectRequest, InitGameResult, CleanGameResult]):
    if isinstance(req, FakeFrontendConnectRequest):
        handle_connect(req)
    elif isinstance(req, InitGameResult):
        handle_init(req)
    elif isinstance(req, CleanGameResult):
        handle_clean(req)
