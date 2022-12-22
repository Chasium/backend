from apigen.generated.ws.connect import WsConnectRequest, WsConnectResponse
from http_api.auth.util import get_user
from ws_api import ws_api
from flask_socketio import join_room


def connect(req: WsConnectRequest):
    res = WsConnectResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return
    join_room(req.session)
    res.solve__code(0)
    res.emit_to_room(req.session)
