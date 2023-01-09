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
from db.models.card import CardTemplateData

from apigen.generated.card_template.get import CardTemplate


class CardTemplateTestCase(unittest.TestCase):

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

    def test_create_template(self):
        # bad session
        data = {'session': '',
                'name': 'template1', 'template': '', 'scripts': ['']}
        response = self.alice.post(
            '/card-template/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)

        # template existed
        data = {'session': self.alice_session,
                'name': 'template1', 'template': '', 'scripts': ['']}
        response = self.alice.post(
            '/card-template/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)

        # success
        data = {'session': self.bob_session,
                'name': 'template1', 'template': '', 'scripts': ['']}
        response = self.bob.post(
            '/card-template/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

        # try create card
        response = self.bob.post(
            '/card-template/get-mine',
            json={'session': self.bob_session, 'page': 1, 'pageSize': 5}
        )
        json_data = json.loads(response.data)
        templates: List[CardTemplateData] = json_data['templates']
        self.assertEqual(len(templates), 1)
        temp_id = templates[0]['id']

        data = {'session': self.bob_session,
                'name': 'card1', 'card': '', 'templateId': temp_id}
        response = self.bob.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

    def test_edit_template(self):
        # bad session
        data = {'session': '',
                'id': self.templateId, 'template': 'testing', 'scripts': ['a', 'b']}
        response = self.alice.post(
            '/card-template/edit',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)

        # template not existed
        data = {'session': self.alice_session,
                'id': -1, 'template': 'testing', 'scripts': ['a', 'b']}
        response = self.alice.post(
            '/card-template/edit',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)

        # success
        data = {'session': self.alice_session,
                'id': self.templateId, 'template': 'testing', 'scripts': ['a', 'b']}
        response = self.alice.post(
            '/card-template/edit',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

        # check template modified
        response = self.alice.post(
            '/card-template/get-mine',
            json={'session': self.alice_session, 'page': 1, 'pageSize': 5}
        )
        json_data = json.loads(response.data)
        templates: List[CardTemplate] = json_data['templates']
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0]['value'], 'testing')
        self.assertEqual(templates[0]['scripts'], ['a', 'b'])

    def test_delete_template(self):
        # bad session
        data = {'session': '', 'id': self.templateId}
        response = self.alice.post(
            '/card-template/delete',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)

        # template not existed
        data = {'session': self.bob_session, 'id': self.templateId}
        response = self.alice.post(
            '/card-template/delete',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)

        # success
        data = {'session': self.alice_session, 'id': self.templateId}
        response = self.alice.post(
            '/card-template/delete',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

        # try create card
        data = {'session': self.alice_session,
                'name': 'card1', 'card': '', 'templateId': self.templateId}
        response = self.alice.post(
            '/card/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)

    def test_get_by_id(self):
        # bad session
        data = {'session': '', 'id': self.templateId}
        response = self.alice.post(
            '/card-template/get-by-id',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)
        self.assertEqual(json_data['template'], None)

        # template not existed
        data = {'session': self.alice_session, 'id': -1}
        response = self.alice.post(
            '/card-template/get-by-id',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)
        self.assertEqual(json_data['template'], None)

        # success
        data = {'session': self.alice_session, 'id': self.templateId}
        response = self.alice.post(
            '/card-template/get-by-id',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        template: CardTemplate = json_data['template']
        self.assertEqual(template['id'], self.templateId)

    def test_get_template(self):
        # bob create template
        data = {'session': self.bob_session,
                'name': 'template1', 'template': 't', 'scripts': ['']}
        response = self.bob.post(
            '/card-template/create',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)

        # get all
        response = self.alice.post(
            '/card-template/get',
            json={'session': self.alice_session, 'page': 1, 'pageSize': 5}
        )
        json_data = json.loads(response.data)
        templates: List[CardTemplateData] = json_data['templates']
        self.assertEqual(len(templates), 2)
        self.assertEqual(templates[0]['name'], 'template1')
        self.assertEqual(templates[1]['name'], 'template1')

        # bad session
        response = self.alice.post(
            '/card-template/get',
            json={'session': '', 'page': 1, 'pageSize': 5}
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)

        # get-mine
        response = self.alice.post(
            '/card-template/get-mine',
            json={'session': self.alice_session, 'page': 1, 'pageSize': 5}
        )
        json_data = json.loads(response.data)
        templates: List[CardTemplate] = json_data['templates']
        self.assertEqual(len(templates), 1)
        a_name = templates[0]['name']
        a_id = templates[0]['id']

        response = self.bob.post(
            '/card-template/get-mine',
            json={'session': self.bob_session, 'page': 1, 'pageSize': 5}
        )
        json_data = json.loads(response.data)
        templates: List[CardTemplate] = json_data['templates']
        self.assertEqual(len(templates), 1)
        b_name = templates[0]['name']
        b_id = templates[0]['id']

        self.assertEqual(a_name, b_name)
        self.assertNotEqual(a_id, b_id)
        self.assertEqual(self.templateId, a_id)
        self.assertNotEqual(self.templateId, b_id)


if __name__ == '__main__':
    unittest.main()
