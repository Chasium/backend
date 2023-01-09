# -*- coding: utf-8 -*-
import unittest
from db import db
from http_api import http_api
import config

from tests.auth.test_user_util import UserUtilsTestCase
from tests.auth.test_user import UserAuthTestCase

from tests.room.test_join import RoomTestCase
from tests.room.test_list import RoomListTestCase
from tests.room.test_chat import ChatTestCase

from tests.card.test_card import CardTestCase
from tests.card_template.test_card_template import CardTemplateTestCase


def suite():
    http_api.config.from_object(config)
    http_api.testing = True
    db.init_app(http_api)

    suite = unittest.TestSuite()
    suite.addTest(UserUtilsTestCase('test_register_params_check'))

    suite.addTest(UserAuthTestCase('test_login_api'))
    suite.addTest(UserAuthTestCase('test_logout_api'))
    suite.addTest(UserAuthTestCase('test_register_api'))

    suite.addTest(RoomTestCase('test_create_room'))
    suite.addTest(RoomTestCase('test_join_room'))
    suite.addTest(RoomTestCase('test_quit_room'))

    suite.addTest(RoomListTestCase('test_get_list'))

    suite.addTest(ChatTestCase('test_room_chat'))

    suite.addTest(CardTestCase('test_create_card'))
    suite.addTest(CardTestCase('test_delete_card'))
    suite.addTest(CardTestCase('test_get_card'))

    suite.addTest(CardTemplateTestCase('test_create_template'))
    suite.addTest(CardTemplateTestCase('test_edit_template'))
    suite.addTest(CardTemplateTestCase('test_delete_template'))
    suite.addTest(CardTemplateTestCase('test_get_by_id'))
    suite.addTest(CardTemplateTestCase('test_get_template'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
