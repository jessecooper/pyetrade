#!/usr/bin/env python3
'''pyetrade market unit tests - a good tutorial for unittest is shown in https://www.youtube.com/watch?v=FxSsnHeWQBY
   TODO:
       * lint
'''

import unittest
from unittest.mock import patch
import datetime as dt
import json
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
           
        response = [ { 'symbol': 'AAPL',
                       'description': 'interesting article',
                       'type': 'EQUITY'
                       },
                     { 'symbol': 'GOOGL',
                       'description': 'another interesting article',
                       'type': 'EQUITY'
                       }]
        response_array = [ {'Data': x} for x in response ]
        JSON_response = json.dumps({'LookupResponse': response_array} )
        XML_response = r'<xml>interesting article</xml>'
        
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
           
        response =  [ { 'dateTime': '15:17:00 EDT 06-20-2018',
                        'dateTimeUTC': 1529522220,
                        'All': { 'open': 1188.34 },
                        'Product': { 'symbol': 'AAPL' }
                      } ]
        response_dict =  { 'QuoteData': response }
        JSON_response = json.dumps({'QuoteResponse': response_dict})
        XML_response = r'<xml> xml text </xml>'
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().return_value = JSON_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test prod Get Qoute
        self.assertEqual(mark.get_quote(['AAPL']), response)
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
           
        response = [ dt.date(2018,11,16), dt.date(2018,12,18) ]
        date_list = [ {'ExpirationDate': { 'year': str(x.year), 'month': str(x.month), 'day': str(x.day), 'expiryType': 'MONTHLY' }} for x in response ]
        json_obj = { 'OptionExpireDateResponse': date_list }
        JSON_response = json.dumps(json_obj)
        XML_response = r'<xml> xml text </xml>'
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().return_value = JSON_response
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
        
        option_pairs =  [ { 'Call': { 'symbol': 'AAPL', 'volume': 23 }, 'Put': { 'symbol': 'AAPL', 'volume': 45 } },
                          { 'Call': { 'symbol': 'GOOGL', 'volume': 15 }, 'Put': { 'symbol': 'GOOGL', 'volume': 111 } }
                        ]
        response = [ {'OptionPair': x} for x in option_pairs ]
        JSON_response = json.dumps(response)
        XML_response = r'<xml> xml text </xml>'
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().return_value = JSON_response
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
        