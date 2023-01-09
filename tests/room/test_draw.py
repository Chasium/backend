'''
    This test is not finished.
'''
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
from apigen.generated.room.draw import (
    DrawRequest, DrawResponse, ClearRequest, ClearResponse,
    UpdateBgRequest, UpdateBgResponse
)

from ws_api.room.join import handle_create, handle_quit
from ws_api.room.chat import chat
from ws_api.room.util import get_user_room


class DrawTestCase(unittest.TestCase):

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

    @patch.object(DrawResponse, 'emit_to_room')
    def test_draw(self, mock0):
        mock0.return_value = None

    @patch.object(ClearResponse, 'emit_to_room')
    def test_clear(self, mock0):
        mock0.return_value = None

    @patch.object(UpdateBgResponse, 'emit_to_room')
    def test_update_bg(self, mock0):
        mock0.return_value = None


if __name__ == '__main__':
    unittest.main()
