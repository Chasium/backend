import unittest
from unittest.mock import patch
import json
from typing import List

from http_api import http_api
from ws_api import ws_api
from db import db
import config

from flask import current_app
from db.models.user import UserData
from db.models.card import CardData, CardTemplateData

from apigen.generated.card.get import Card


class CardTestCase(unittest.TestCase):

    @patch('ws_api.room.join.join_room')
    def setUp(self, mock_join_room):
        mock_join_room.return_value = None

        # http_api.config.from_object(config)
        # http_api.testing = True
        # db.init_app(http_api)
        ws_api.init_app(http_api, cors_allowed_origins="*")
        self.app_context = http_api.app_context()
        self.app_context.push()
        with self.app_context:
            db.drop_all()
            db.create_all()

        user = UserData('alice', 'alice123')
        db.session.add(user)
        template = CardTemplateData('template1', '', user)
        db.session.add(template)
        card = CardData('abc', '', user, template)
        db.session.add(card)
        db.session.commit()

        user = UserData('bob', 'bob123')
        db.session.add(user)
        db.session.commit()

        # login
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

        self.bob = current_app.test_client()
        response = self.bob.post(
            '/auth/login',
            json={"userName": "bob", "password": "bob123"}
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.bob_session = json_data['session']
        self.bob_socket = ws_api.test_client(
            current_app, flask_test_client=self.alice)
        self.assertEqual(self.alice_socket.is_connected(), True)

        # get template id
        response = self.alice.post(
            '/card-template/get-mine',
            json={'session': self.alice_session, 'page': 1, 'pageSize': 5}
        )
        json_data = json.loads(response.data)
        templates: List[CardTemplateData] = json_data['templates']
        self.assertEqual(len(templates), 1)
        self.templateId = templates[0]['id']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_card(self):
        # bad session
        data = {'session': '', 'name': 'card1',
                'card': '', 'templateId': self.templateId}
        response = self.alice.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)

        # template not existed
        data = {'session': self.alice_session,
                'name': 'card1', 'card': '', 'templateId': -1}
        response = self.alice.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)

        # success
        data = {'session': self.alice_session,
                'name': 'card1', 'card': '', 'templateId': self.templateId}
        response = self.alice.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

        # card is existed
        data = {'session': self.alice_session,
                'name': 'card1', 'card': '', 'templateId': self.templateId}
        response = self.alice.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 3)

        data = {'session': self.alice_session, 'page': 1, 'pageSize': 5}
        response = self.alice.post(
            '/card/get',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        cards: List[Card] = json_data['cards']
        self.assertEqual(len(cards), 2)
        self.assertIn(cards[0]['name'], {'abc', 'card1'})
        self.assertIn(cards[1]['name'], {'abc', 'card1'})

        # bob create card using alice's template
        data = {'session': self.bob_session,
                'name': 'card1', 'card': '', 'templateId': self.templateId}
        response = self.bob.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

    def test_delete_card(self):
        data = {'session': self.alice_session, 'page': 1, 'pageSize': 5}
        response = self.alice.post(
            '/card/get',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        cards: List[Card] = json_data['cards']
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['name'], 'abc')

        # bad session
        data = {'session': '', 'id': cards[0]['id']}
        response = self.alice.post(
            '/card/delete',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)

        # success
        data = {'session': self.alice_session, 'id': cards[0]['id']}
        response = self.alice.post(
            '/card/delete',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

        # card not existed
        response = self.alice.post(
            '/card/delete',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)

        # get nothing
        data = {'session': self.alice_session, 'page': 1, 'pageSize': 5}
        response = self.alice.post(
            '/card/get',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.assertEqual(json_data['pages'], 0)
        cards: List[Card] = json_data['cards']
        self.assertEqual(len(cards), 0)

    def test_get_card(self):
        # bad session
        data = {'session': '', 'page': 1, 'pageSize': 5}
        response = self.alice.post(
            '/card/get',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)

        # bob creates card
        data = {'session': self.bob_session,
                'name': 'abc', 'card': '', 'templateId': self.templateId}
        response = self.bob.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

        # get all cards
        data = {'session': self.alice_session, 'page': 1, 'pageSize': 5}
        response = self.alice.post(
            '/card/get',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.assertEqual(json_data['pages'], 1)
        cards: List[Card] = json_data['cards']
        self.assertEqual(len(cards), 2)

        # get alice's card
        data = {'session': self.alice_session, 'page': 1, 'pageSize': 5}
        response = self.alice.post(
            '/card/get-mine',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.assertEqual(json_data['pages'], 1)
        cards: List[Card] = json_data['cards']
        self.assertEqual(len(cards), 1)


if __name__ == '__main__':
    unittest.main()
