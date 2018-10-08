#!/usr/bin/env python3
'''pyetrade market unit tests
   TODO:
       * lint'''

import string
import random
import unittest
from unittest.mock import patch
from pyetrade import market

class TestETradeMarket(unittest.TestCase):
    '''TestEtradeMarket Unit Test'''
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_look_up_product(self, MockOAuthSession):
        '''test_look_up_product(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'BAC': '32.10'}"
        MockOAuthSession().get().text = r'<xml> returns </xml>'
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test Get Quote
        self.assertEqual(
            mark.look_up_product('Bank Of', 'EQ'),
            "{'BAC': '32.10'}"
            )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        # Test Get Qoute xml
        self.assertEqual(mark.look_up_product('Back Of', 'EQ', resp_format='xml'),
                         r"<xml> returns </xml>")
        self.assertTrue(MockOAuthSession().get.called)
        # Test Prod Get Qoute
        self.assertEqual(mark.look_up_product('Bank Of', 'EQ'),
                         "{'BAC': '32.10'}")
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        # Test prod Get Qoute xml
        self.assertEqual(mark.look_up_product('Back Of', 'EQ', resp_format='xml'),
                         r"<xml> returns </xml>")
        self.assertTrue(MockOAuthSession().get.called)
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_quote(self, MockOAuthSession):
        '''test_get_quote(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'BAC': '32.10'}"
        MockOAuthSession().get().text = r'<xml> returns </xml>'
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test prod Get Qoute
        self.assertEqual(mark.get_quote('BAC'), "{'BAC': '32.10'}")
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        # Test prod Get Qoute xml
        self.assertEqual(mark.get_quote('BAC', resp_format='xml'),
                         r"<xml> returns </xml>")
        self.assertTrue(MockOAuthSession().get.called)

    @patch('pyetrade.market.OAuth1Session')
    def test_get_quote_exception(self, MockOAuthSession):
        '''test_get_quote(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session'''
        # Generate symboles
        sym = [''.join(random.choice(string.ascii_uppercase) \
               for _ in range(3)) for _ in range(30)]
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)

        # Test exception class
        mark.get_quote(sym)
