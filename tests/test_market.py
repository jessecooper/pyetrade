#!/usr/bin/env python3
'''pyetrade market unit tests
   TODO:
       * lint'''

import string
import random
import pytest
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
           description: MagicMock of OAuth1Session
        '''
           
        response = {'BAC': '32.10'}
        
        # Set Mock returns
        MockOAuthSession().get().json.return_value = response
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        
        # Test Get Quote JSON
        self.assertEqual(mark.look_up_product('Bank Of', 'EQ'), response )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Test Get Quote xml
        self.assertEqual(mark.look_up_product('Back Of', 'EQ', resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_quote(self, MockOAuthSession):
        '''test_get_quote(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        '''
           
        response = {'BAC': '32.10'}
        
        # Set Mock returns
        MockOAuthSession().get().json.return_value = response
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        
        # Test prod Get Qoute
        self.assertEqual(mark.get_quote(['BAC']), response)
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Test prod Get Qoute xml
        self.assertEqual(mark.get_quote(['BAC'], resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Test log message if more than 25 quotes are requested
        # Generate 30 symbols; response should only be 25 symbols
        sym = [''.join(random.choice(string.ascii_uppercase) for _ in range(3)) for _ in range(30)]
        retn = {x:32.1 for x in sym[:25]}
        MockOAuthSession().get().json.return_value = retn
        self.assertEqual(mark.get_quote(sym), retn)
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Test exception class
#        sym = [''.join(random.choice(string.ascii_uppercase) for _ in range(3)) for _ in range(25)]
#        self.assertRaises(requests.exceptions.HTTPError, mark.get_quote, sym)

    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_option_expire_date(self, MockOAuthSession):
        '''test_get_optionexpiredate(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session'''
        # Set Mock returns
        MockOAuthSession().get().return_value = [ dt.date(2018,10,19) ]
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_expire_date('AAPL'), [ dt.date(2018,10,19) ])
        self.assertTrue(MockOAuthSession().get.called)
  
