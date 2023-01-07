# -*- coding: utf-8 -*-
import unittest

from tests.auth.test_user_util import UserUtilsTestCase
from tests.auth.test_user_interaction import UserInteractionTestCase
from tests.auth.test_user import UserAuthTestCase

from tests.room.test_join import RoomTestCase
from tests.room.test_list import RoomListTestCase
from tests.room.test_chat import ChatTestCase


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(UserUtilsTestCase('test_register_params_check'))
    # suite.addTest(UserInteractionTestCase('test_user_interaction'))

    # BUG: can't test together
    # suite.addTest(UserAuthTestCase('test_login_api'))
    # suite.addTest(UserAuthTestCase('test_logout_api'))
    # BUG: apigen register circular import
    # suite.addTest(UserAuthTestCase('test_register_api'))

    # suite.addTest(RoomTestCase('test_create_room'))
    # suite.addTest(RoomTestCase('test_join_room'))
    # suite.addTest(RoomTestCase('test_quit_room'))

    # suite.addTest(RoomListTestCase('test_get_list'))

    suite.addTest(ChatTestCase('test_room_chat'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
