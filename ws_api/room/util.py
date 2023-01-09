from typing import Dict
from random import getrandbits


class Room:
    id: str
    fake_frontend_id: int
    player_card_map: Dict[str, str]
    player_card_id_map: Dict[str, str]
    prepare_map: Dict[str, bool]
    template_id: int
    host_name: str

    def __init__(self, host_name: str):
        self.id = hex(getrandbits(128))
        self.player_card_map = {}
        self.player_card_id_map = {}
        self.prepare_map = {}
        self.fake_frontend_id = -1
        self.host_name = host_name

    def get_users(self):
        return list(self.player_card_map.keys())


room_dict: Dict[str, Room] = {}
session_room_dict: Dict[str, Room] = {}


def get_room(id: str):
    try:
        return room_dict[id]
    except KeyError:
        return None


def get_user_room(session: str):
    try:
        return session_room_dict[session]
    except KeyError:
        return None


def create_room(session: str, user_name: str) -> Room:
    room = Room(user_name)
    room_dict[room.id] = room
    session_room_dict[session] = room
    return room


def user_join_room(session: str, user_name: str, room_id: str):
    room = room_dict[room_id]
    room.player_card_map[user_name] = ''
    room.prepare_map[user_name] = False
    room.player_card_id_map[user_name] = -1
    session_room_dict[session] = room


def quit_room(session: str, user_name: str):
    room = session_room_dict[session]
    session_room_dict.pop(session)
    room.player_card_map.pop(user_name, '')
    room.prepare_map.pop(user_name, False)
    room.player_card_id_map.pop(user_name, -1)


def delete_room(session: str, room_id: str):
    session_room_dict.pop(session)
    room_dict.pop(room_id)
