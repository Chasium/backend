from apigen.generated.room.draw import DrawRequest, DrawResponse, ClearRequest, ClearResponse, UpdateBgRequest, UpdateBgResponse
from typing import Union
from ws_api.room.util import get_user_room


def handle_draw(req: DrawRequest):
    room = get_user_room(req.session)
    if room is None:
        return
    res = DrawResponse()
    res.solve__x(req.x)
    res.solve__y(req.y)
    res.solve__color(req.color)
    res.solve__type(req.type)
    res.emit_to_room(room.id)


def handle_clear(req: ClearRequest):
    room = get_user_room(req.session)
    if room is None:
        return
    res = ClearResponse()
    res.emit_to_room(room.id)


def handle_update_bg(req: UpdateBgRequest):
    room = get_user_room(req.session)
    if room is None:
        return
    res = UpdateBgResponse()
    res.solve__src(req.src)
    res.emit_to_room(room.id)


def draw(req: Union[DrawRequest, ClearRequest, UpdateBgRequest]):
    if isinstance(req, DrawRequest):
        handle_draw(req)
    if isinstance(req, ClearRequest):
        handle_clear(req)
    if isinstance(req, UpdateBgRequest):
        handle_update_bg(req)
