from apigen.generated.room.join import JoinRoomRequest, JoinRoomResponse, CreateRoomRequest, CreateRoomResponse, QuitRoomRequest, QuitRoomResponse
from typing import Union
from http_api.auth.util import get_user, get_session_by_name
from ws_api.room.util import create_room, get_room, user_join_room, get_user_room, quit_room, delete_room
from flask_socketio import join_room, leave_room, close_room


def handle_create(req: CreateRoomRequest):
    res = CreateRoomResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_to_room(None)
        return res.to_json()
    room = get_user_room(req.session)
    if room is not None:
        res.solve__code(2)
        res.emit_back()
        return res.to_json()

    room = create_room(req.session, user.name)
    user_join_room(req.session, user.name, room.id)
    join_room(room.id)
    res.solve__code(0)
    res.solve__room_id(room.id)
    res.emit_to_room(room.id)
    return res.to_json()


def handle_join(req: JoinRoomRequest):
    res = JoinRoomResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return res.to_json()
    room = get_room(req.room)
    if room is None:
        res.solve__code(2)
        res.emit_back()
        return res.to_json()
    room = get_user_room(req.session)
    if room is not None:
        res.solve__code(3)
        res.emit_back()
        return res.to_json()
    join_room(req.room)
    user_join_room(req.session, user.name, req.room)
    room = get_user_room(req.session)

    res.solve__code(0)
    users = room.get_users()
    users.append(room.host_name)
    res.solve__users(users)
    res.solve__host(room.host_name)
    res.emit_to_room(req.room)
    return res.to_json()


def handle_quit(req: QuitRoomRequest):
    res = QuitRoomResponse()
    user = get_user(req.session)
    if user is None:
        res.solve__code(1)
        res.emit_back()
        return res.to_json()

    room = get_user_room(req.session)
    if room is None:
        res.solve__code(2)
        res.emit_back()
        return res.to_json()

    if room.host_name == user.name:
        users = room.get_users()
        print(users)
        for i in users:
            session = get_session_by_name(i)
            quit_room(session, i)
            res.solve__code(0)
            res.solve__user(i)
            res.emit_to_room(session)
        delete_room(room.id)
        close_room(room.id)
        res.solve__code(0)
        res.solve__user(user.name)
        res.emit_back()
        return res.to_json()

    leave_room(room.id)
    quit_room(req.session, user.name)
    res.solve__code(0)
    res.solve__user(user.name)
    res.emit_back()
    res.emit_to_room(room.id)
    return res.to_json()


def join(req: Union[JoinRoomRequest, CreateRoomRequest, QuitRoomRequest]):
    if isinstance(req, CreateRoomRequest):
        handle_create(req)
    elif isinstance(req, JoinRoomRequest):
        handle_join(req)
    else:
        handle_quit(req)
