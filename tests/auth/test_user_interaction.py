import unittest

from http_api import http_api
from db import db
import config

from http_api.auth import util
from db.models.user import UserData


class UserInteractionTestCase(unittest.TestCase):
    def setUp(self):
        http_api.config.from_object(config)
        db.init_app(http_api)
        self.app_context = http_api.app_context()
        self.app_context.push()
        with self.app_context:
            db.create_all()
        self.assertEqual(util.user_exists('test'), False)
        user = UserData('test', 'test123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_interaction(self):
        # user existence
        username = 'test'
        password = 'test123'
        self.assertEqual(util.user_exists(username), True)
        self.assertEqual(util.user_exists(''), False)
        self.assertEqual(util.user_exists('abc'), False)
        util.add_user('abc', password)
        self.assertEqual(util.user_exists('abc'), True)

        # password verification
        self.assertEqual(util.password_verified('', ''), False)
        self.assertEqual(util.password_verified(username, ''), False)
        self.assertEqual(util.password_verified(username, password), True)
        self.assertEqual(util.password_verified('abc', password), True)

        # user login
        self.assertEqual(util.logged_in(username), False)
        temp_session = util.user_login(username)
        self.assertEqual(util.logged_in(username), True)
        self.assertEqual(util.logged_in('abc'), False)

        # user logged
        self.assertEqual(util.user_login(''), None)
        self.assertEqual(util.get_session_by_name(''), None)
        self.assertEqual(util.get_session_by_name('abc'), None)
        self.assertEqual(util.get_session_by_name(username), temp_session)

        # get user data
        self.assertEqual(util.get_user(''), None)
        userdata = util.get_user(temp_session)
        self.assertEqual(userdata.getName(), 'test')
        self.assertEqual(util.get_session(userdata.getId()), temp_session)
