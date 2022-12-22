from apigen.generated.room.chat import ChatRequest, ChatResponse
from http_api.auth.util import get_user
from ws_api.room.util import get_user_room


def chat(req: ChatRequest):
    res = ChatResponse()
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

    res.solve__code(0)
    res.solve__message(req.message)
    res.emit_to_room(room.id)
