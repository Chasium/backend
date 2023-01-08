import unittest
from http_api.auth import util
from http_api import http_api
import config
from db import db
from db.models.user import UserData


class UserUtilsTestCase(unittest.TestCase):

    def test_register_params_check(self):

        # Username
        username = ''
        self.assertEqual(util.username_legal(username), False)
        username = '12'
        self.assertEqual(util.username_legal(username), False)
        username = 'ab3'
        self.assertEqual(util.username_legal(username), True)
        username = 'vnln2v84hvownfkjws8ydiy_UWYhfalu'
        self.assertEqual(util.username_legal(username), True)
        username = 'vnln2v84hvownfkj*s8ydiy_UWYhfalu'
        self.assertEqual(util.username_legal(username), False)
        username = 'vnln2v84hvownfksdfs8ydiy_UWYhfalu'
        self.assertEqual(util.username_legal(username), False)

        # Password
        password = ''
        self.assertEqual(util.password_legal(password), False)
        password = 'abc12'
        self.assertEqual(util.password_legal(password), False)
        password = 'abc123'
        self.assertEqual(util.password_legal(password), True)
        password = 'abc12\/3'
        self.assertEqual(util.password_legal(password), False)
        password = 'GIs4a21~`!@#$%^&*()_-+=[{]}|:;<>'
        self.assertEqual(util.password_legal(password), True)
        password = 'GIs4a121~`!@#$%^&*()_-+=[{]}|:;<>'
        self.assertEqual(util.password_legal(password), False)


if __name__ == '__main__':
    unittest.main()
