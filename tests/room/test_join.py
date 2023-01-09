import unittest
from unittest.mock import patch
import json

from http_api import http_api
from ws_api import ws_api
from db import db
import config

from flask import current_app
from db.models.user import UserData

from apigen.generated.room.join import (
    JoinRoomRequest, JoinRoomResponse, CreateRoomRequest,
    CreateRoomResponse, QuitRoomRequest, QuitRoomResponse
)

from ws_api.room.join import handle_create, handle_join, handle_quit


class RoomTestCase(unittest.TestCase):

    @patch.object(CreateRoomResponse, 'emit_to_room')
    @patch.object(CreateRoomResponse, 'emit_back')
    @patch('ws_api.room.join.join_room')
    def setUp(self, mock0, mock1, mock2):
        mock0.return_value = None
        mock1.return_value = None
        mock2.return_value = None

        http_api.config.from_object(config)
        http_api.testing = True
        # db.init_app(http_api)
        ws_api.init_app(http_api, cors_allowed_origins="*")
        self.app_context = http_api.app_context()
        self.app_context.push()
        with self.app_context:
            db.drop_all()
            db.create_all()

        user = UserData('alice', 'alice123')
        db.session.add(user)
        user = UserData('bob', 'bob123')
        db.session.add(user)
        db.session.commit()

        self.alice = current_app.test_client()
        self.bob = current_app.test_client()

        response = self.alice.post(
            '/auth/login',
            json={"userName": "alice", "password": "alice123"}
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.alice_session = json_data['session']
        self.alice_socket = ws_api.test_client(
            current_app, flask_test_client=self.alice)
        self.assertEqual(self.alice_socket.is_connected(), True)

        response = self.bob.post(
            '/auth/login',
            json={"userName": "bob", "password": "bob123"}
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.bob_session = json_data['session']
        self.bob_socket = ws_api.test_client(
            current_app, flask_test_client=self.bob)
        self.assertEqual(self.bob_socket.is_connected(), True)

        # alice create room
        data = {"session": self.alice_session}
        response = handle_create(CreateRoomRequest.from_request(data))
        self.assertEqual(response['code'], 0)
        self.assertNotEqual(response['roomId'], None)
        self.alice_room = response['roomId']

    @patch.object(QuitRoomResponse, 'emit_to_room')
    @patch.object(QuitRoomResponse, 'emit_back')
    @patch('ws_api.room.join.close_room')
    def tearDown(self, mock0, mock1, mock2):
        mock0.return_value = None
        mock1.return_value = None
        mock2.return_value = None

        data = {"session": self.alice_session}
        response = handle_quit(QuitRoomRequest.from_request(data))
        data = {"session": self.bob_session}
        response = handle_quit(QuitRoomRequest.from_request(data))

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch.object(CreateRoomResponse, 'emit_to_room')
    @patch.object(CreateRoomResponse, 'emit_back')
    @patch('ws_api.room.join.join_room')
    def test_create_room(self, mock_join_room, mock_emit_back, mock_emit_to_room):
        mock_join_room.return_value = None
        mock_emit_back.return_value = None
        mock_emit_to_room.return_value = None

        # fail
        data = {"session": ''}
        response = handle_create(CreateRoomRequest.from_request(data))
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['roomId'], None)

        # create again
        data = {"session": self.alice_session}
        response = handle_create(CreateRoomRequest.from_request(data))
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['roomId'], None)

        # success
        data = {"session": self.bob_session}
        response = handle_create(CreateRoomRequest.from_request(data))
        self.assertEqual(response['code'], 0)
        self.assertNotEqual(response['roomId'], None)

    @patch.object(JoinRoomResponse, 'emit_to_room')
    @patch.object(JoinRoomResponse, 'emit_back')
    @patch('ws_api.room.join.join_room')
    def test_join_room(self, mock_join_room, mock_emit_back, mock_emit_to_room):
        mock_join_room.return_value = None
        mock_emit_back.return_value = None
        mock_emit_to_room.return_value = None

        # joined
        data = {"session": self.alice_session, 'room': self.alice_room}
        response = handle_join(JoinRoomRequest.from_request(data))
        self.assertEqual(response['code'], 3)
        self.assertEqual(response['users'], None)
        self.assertEqual(response['host'], None)

        # bad session
        data = {"session": '', 'room': self.alice_room}
        response = handle_join(JoinRoomRequest.from_request(data))
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['users'], None)
        self.assertEqual(response['host'], None)

        # room not existed
        data = {"session": self.bob_session, 'room': ''}
        response = handle_join(JoinRoomRequest.from_request(data))
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['users'], None)
        self.assertEqual(response['host'], None)

        # success
        data = {"session": self.bob_session, 'room': self.alice_room}
        response = handle_join(JoinRoomRequest.from_request(data))
        self.assertEqual(response['code'], 0)
        self.assertEqual(len(response['users']), 2)
        self.assertEqual(response['host'], 'alice')

    @patch.object(JoinRoomResponse, 'emit_to_room')
    @patch.object(JoinRoomResponse, 'emit_back')
    @patch.object(QuitRoomResponse, 'emit_to_room')
    @patch.object(QuitRoomResponse, 'emit_back')
    @patch('ws_api.room.join.close_room')
    @patch('ws_api.room.join.join_room')
    def test_quit_room(self, mock0, mock1, mock2, mock3, mock4, mock5):
        mock0.return_value = None
        mock1.return_value = None
        mock2.return_value = None
        mock3.return_value = None
        mock4.return_value = None
        mock5.return_value = None

        data = {"session": self.bob_session, 'room': self.alice_room}
        response = handle_join(JoinRoomRequest.from_request(data))
        self.assertEqual(response['code'], 0)

        # bad session
        data = {"session": ''}
        response = handle_quit(QuitRoomRequest.from_request(data))
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['user'], None)

        # success
        data = {"session": self.alice_session}
        response = handle_quit(QuitRoomRequest.from_request(data))
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['user'], 'alice')

        # not joined
        data = {"session": self.alice_session}
        response = handle_quit(QuitRoomRequest.from_request(data))
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['user'], None)

        data = {"session": self.bob_session}
        response = handle_quit(QuitRoomRequest.from_request(data))
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['user'], None)


if __name__ == '__main__':
    unittest.main()
