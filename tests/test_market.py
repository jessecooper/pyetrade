#!/usr/bin/env python3
'''pyetrade market unit tests - a good tutorial for unittest is shown in https://www.youtube.com/watch?v=FxSsnHeWQBY
   TODO:
       * lint
'''

import unittest
from unittest.mock import patch
import datetime as dt
from pyetrade import market

  
class TestETradeMarket(unittest.TestCase):
    '''TestEtradeMarket Unit Test'''
    
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_look_up_product(self, MockOAuthSession):
        '''test_look_up_product(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
           
           3 tests based on resp_format = (None,'xml','json')
           test exception raised when resp_format is something different from three choices
        '''
           
        response = ['interesting article']
        XML_response = r'<xml>interesting article</xml>'
        JSON_response = r'["interesting article"]'
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().return_value = JSON_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test Get Quote returning python list
        self.assertEqual(mark.look_up_product('Bank Of', resp_format=None), response )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test Get Quote returning xml
        self.assertEqual(mark.look_up_product('Bank Of', resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=json
        MockOAuthSession().get().return_value = JSON_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test Get Quote returning json
        self.assertEqual(mark.look_up_product('Bank Of', resp_format='json'), JSON_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # test exception when wrong resp_format supplied
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertRaises(AssertionError, mark.look_up_product, 'Bank Of', resp_format='idiot')
        
        
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_quote(self, MockOAuthSession):
        '''test_get_quote(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        '''
           
        response = {'BAC': 32.1}
        XML_response = r'<xml> xml text </xml>'
        JSON_response = r'{"BAC": 32.1}'
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().return_value = JSON_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test prod Get Qoute
        self.assertEqual(mark.get_quote(['BAC']), response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test prod Get Qoute xml
        self.assertEqual(mark.get_quote(['BAC'], resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=json
        MockOAuthSession().get().return_value = JSON_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test prod Get Qoute json
        self.assertEqual(mark.get_quote(['BAC'], resp_format='json'), JSON_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # test exception when wrong resp_format supplied
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertRaises(AssertionError, mark.get_quote, ['BAC'], resp_format='idiot')
        
        # test the assertion failure of detail_flag, requireEarningsDate, skipMiniOptionsCheck
        
        # Test log message if more than 25 quotes are requested
        # Generate 30 symbols; response should only be 25 symbols
        sym = 30*['AAPL']
        retn = {x:32.1 for x in sym[:25]}
        MockOAuthSession().get().return_value = retn
        self.assertEqual(mark.get_quote(sym), retn)
        self.assertTrue(MockOAuthSession().get.called)
        
        
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_option_expire_date(self, MockOAuthSession):
        '''test_get_optionexpiredate(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        '''
           
        response = [ dt.date(2018,10,19) ]
        XML_response = r'<xml> xml text </xml>'
        JSON_response = r'"JSON text"'
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().return_value = response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_expire_date('AAPL', resp_format=None), response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_expire_date('AAPL', resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=json
        MockOAuthSession().get().return_value = JSON_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_expire_date('AAPL', resp_format='json'), JSON_response)
        self.assertTrue(MockOAuthSession().get.called)
  

    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_option_chains(self, MockOAuthSession):
        '''test_get_optionexpiredate(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        '''
           
        response = [ { 'this_date': 32.1 } ]
        XML_response = r'<xml> xml text </xml>'
        JSON_response = r'"JSON text"'
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().return_value = response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_chains('AAPL', expiry_date=None, resp_format=None), response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_chains('AAPL', expiry_date=None, resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=json
        MockOAuthSession().get().return_value = JSON_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_chains('AAPL', expiry_date=None, resp_format='json'), JSON_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # test the assertion failure of chainType, optionCategory, priceType, skipAdjusted
        