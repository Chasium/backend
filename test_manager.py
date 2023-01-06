# -*- coding: utf-8 -*-
import unittest

from tests.http_api.test_user_util import UserUtilsTestCase
from tests.http_api.test_user_interaction import UserInteractionTestCase


def suite():
    suite = unittest.TestSuite()
    suite.addTest(UserUtilsTestCase('test_register_params_check'))
    suite.addTest(UserInteractionTestCase('test_user_interaction'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
