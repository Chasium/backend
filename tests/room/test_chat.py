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
    QuitRoomRequest, QuitRoomResponse, CreateRoomRequest,
    CreateRoomResponse
)
from apigen.generated.room.chat import ChatRequest, ChatResponse

from ws_api.room.join import handle_create, handle_quit
from ws_api.room.chat import chat
from ws_api.room.util import get_user_room


class ChatTestCase(unittest.TestCase):

    @patch('ws_api.room.join.join_room')
    def setUp(self, mock_join_room):
        mock_join_room.return_value = None

        http_api.config.from_object(config)
        http_api.testing = True
        db.init_app(http_api)
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

        # alice create room
        data = {"session": self.alice_session}
        response = handle_create(CreateRoomRequest.from_request(data))
        self.assertEqual(response['code'], 0)
        self.assertNotEqual(response['roomId'], None)
        self.alice_room = response['roomId']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch.object(QuitRoomResponse, 'emit_to_room')
    @patch.object(QuitRoomResponse, 'emit_back')
    @patch.object(ChatResponse, 'emit_to_room')
    @patch.object(ChatResponse, 'emit_back')
    @patch('ws_api.room.join.close_room')
    @patch('ws_api.room.join.join_room')
    def test_room_chat(self, mock0, mock1, mock2, mock3, mock4, mock5):
        mock0.return_value = None
        mock1.return_value = None
        mock2.return_value = None
        mock3.return_value = None
        mock4.return_value = None
        mock5.return_value = None

        # bad session
        data = {"session": '', "message": 'Hello, world!'}
        response = chat(ChatRequest.from_request(data))
        self.assertEqual(response['code'], 1)
        self.assertEqual(response['message'], None)

        # chat success
        data = {"session": self.alice_session, "message": 'Hello, world!'}
        response = chat(ChatRequest.from_request(data))
        self.assertEqual(response['code'], 0)
        self.assertEqual(response['message'], 'Hello, world!')

        # quit room
        data = {"session": self.alice_session}
        response = handle_quit(QuitRoomRequest.from_request(data))
        self.assertEqual(response['code'], 0)
        self.assertEqual(get_user_room(self.alice_session), None)

        # chat failed
        data = {"session": self.alice_session, "message": 'Hello, world!'}
        response = chat(ChatRequest.from_request(data))
        self.assertEqual(response['code'], 2)
        self.assertEqual(response['message'], None)
