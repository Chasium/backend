from typing import List
from apigen.generated.room.list import ListRoomsRequest, ListRoomsResponse, RoomData
from http_api.auth.util import get_user
from ws_api.room.util import room_dict


def list(req: ListRoomsRequest):
    res = ListRoomsResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        return res

    rooms: List[RoomData] = []
    for i in room_dict:
        temp = RoomData()
        room = room_dict[i]
        temp.solve__id(i)
        temp.solve__users(len(room.get_users()))
        rooms.append(temp)
    res.solve__code(0)
    res.solve__rooms(rooms)
    return res
