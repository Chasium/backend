import unittest
import json

from http_api import http_api
from ws_api import ws_api
from db import db
import config

from flask import current_app, url_for
from db.models.user import UserData

from http_api.auth.util import logged_in, user_exists


class UserAuthTestCase(unittest.TestCase):
    def setUp(self):
        http_api.config.from_object(config)
        http_api.testing = True
        db.init_app(http_api)
        ws_api.init_app(http_api, cors_allowed_origins="*")
        self.app_context = http_api.app_context()
        self.app_context.push()
        with self.app_context:
            db.create_all()

        user = UserData('alice', 'alice123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_api(self):
        client = current_app.test_client()
        # user not exist
        data = {"userName": "bob", "password": "bob123"}
        response = client.post(
            '/auth/login',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 1)
        self.assertEqual(json_data['session'], None)
        self.assertEqual(logged_in('bob'), False)

        # wrong password
        data = {"userName": "alice", "password": "bob123"}
        response = client.post(
            '/auth/login',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 2)
        self.assertEqual(json_data['session'], None)
        self.assertEqual(logged_in('alice'), False)

        # success
        data = {"userName": "alice", "password": "alice123"}
        response = client.post(
            '/auth/login',
            json=data
        )
        json_data = json.loads(response.data)
        temp_session = json_data['session']
        self.assertEqual(json_data['code'], 0)
        self.assertNotEqual(json_data['session'], None)
        self.assertEqual(logged_in('alice'), True)

        # logged in
        data = {"userName": "alice", "password": "alice123"}
        response = client.post(
            '/auth/login',
            json=data
        )
        json_data = json.loads(response.data)
        # BUG
        # self.assertEqual(json_data['code'], 3)
        self.assertEqual(json_data['session'], temp_session)
        self.assertEqual(logged_in('alice'), True)

    def test_logout_api(self):
        client = current_app.test_client()

        data = {"session": "aIUGDKTisff749839ejbsid"}
        response = client.post(
            '/auth/logout',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertNotEqual(json_data['code'], 0)

        response = client.post(
            '/auth/login',
            json={"userName": "alice", "password": "alice123"}
        )
        json_data = json.loads(response.data)
        temp_session = json_data['session']
        self.assertEqual(logged_in('alice'), True)

        response = client.post(
            '/auth/logout',
            json={"session": temp_session}
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.assertEqual(logged_in('alice'), False)

    def test_register_api(self):
        client = current_app.test_client()
        # invalid username
        data = {"userName": "", "password": "alice123"}
        response = client.post(
            '/auth/register',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 10)
        self.assertEqual(user_exists(""), False)

        # user existed
        data = {"userName": "alice", "password": "abc"}
        response = client.post(
            '/auth/register',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 11)
        self.assertEqual(user_exists('alice'), True)

        # invalid password
        data = {"userName": "bob", "password": "123/ab"}
        response = client.post(
            '/auth/register',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 20)
        self.assertEqual(user_exists('bob'), False)

        # invalid password
        data = {"userName": "bob", "password": "bob123"}
        response = client.post(
            '/auth/register',
            json=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['code'], 0)
        self.assertEqual(user_exists('bob'), True)
