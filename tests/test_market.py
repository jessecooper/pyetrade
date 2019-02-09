#!/usr/bin/env python3
'''pyetrade market unit tests - a good tutorial for unittest is shown in https://www.youtube.com/watch?v=FxSsnHeWQBY
   TODO:
       * lint
'''
import sys
import os
import unittest
import datetime as dt
import xml.etree.ElementTree as ET
from unittest.mock import patch
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
           
           3 tests based on resp_format = (None,'xml')
           test exception raised when resp_format is something different from two choices
        '''
           
        response = [{'symbol': 'MMM', 'description': '3M CO COM', 'type': 'EQUITY'}]
        XML_response =  r'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                            <LookupResponse>
                                <Data><symbol>MMM</symbol><description>3M CO COM</description><type>EQUITY</type></Data>
                            </LookupResponse>'''
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test Get Quote returning python list
        self.assertEqual(mark.look_up_product('mmm', resp_format=None), response )
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test Get Quote returning xml
        self.assertEqual(mark.look_up_product('mmm', resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # test exception when wrong resp_format supplied
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertRaises(AssertionError, mark.look_up_product, 'mmm', resp_format='idiot')
        
        
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_quote(self, MockOAuthSession):
        '''test_get_quote(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        '''
           
        response =  [ {'securityType': 'EQ',
                       'symbol': 'MMM',
                       'dateTimeUTC': 1546545180,
                       'adjustedFlag': 'false',
                       'annualDividend': 0.0,
                       'averageVolume': 3078683.0} ]
        XML_response =  r'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><QuoteResponse>
                            <QuoteData><dateTime>14:53:00 EST 01-03-2019</dateTime><dateTimeUTC>1546545180</dateTimeUTC>
                            <All>
                            <adjustedFlag>false</adjustedFlag><annualDividend>0.0</annualDividend>
                            <averageVolume>3078683</averageVolume></All>
                            <Product><securityType>EQ</securityType><symbol>MMM</symbol></Product>
                            </QuoteData></QuoteResponse>
                         '''
#        ET_response = ET.fromstring(XML_response)
        
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().text = XML_response
#        MockOAuthSession().fromstring().return_value = ET_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_quote(['MMM'], resp_format=None), response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test prod Get Qoute xml
        self.assertEqual(mark.get_quote(['MMM'], resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)

        # test exception when wrong resp_format supplied
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertRaises(AssertionError, mark.get_quote, ['MMM'], resp_format='idiot')
        
        # test the assertion failure of detail_flag, requireEarningsDate, skipMiniOptionsCheck
        
    # Mock out OAuth1Session
    @patch('pyetrade.market.OAuth1Session')
    def test_get_option_chains(self, MockOAuthSession):
        '''test_get_optionexpiredate(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        '''
        
        response = [ { 'timeStamp': 1546546266, 'bid': 41.55, 'OptionGreeks': {'iv': 0.6716}} ]
        XML_response = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><OptionChainResponse><OptionPair><Call>
                           <timeStamp>1546546266</timeStamp><bid>41.55</bid>
                           <OptionGreeks><iv>0.435700</iv></OptionGreeks></Call>
                           </OptionPair></OptionChainResponse>
                        '''

        # Set Mock returns for resp_format=None
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_chains('AAPL', expiry_date=dt.date(2019, 2, 15), resp_format=None), response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_chains('AAPL', expiry_date=dt.date(2019, 2, 15), resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # test the assertion failure of chainType, optionCategory, priceType, skipAdjusted
            
    @patch('pyetrade.market.OAuth1Session')
    def test_get_option_expire_date(self, MockOAuthSession):
        '''test_get_optionexpiredate(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        '''
           
        response = [ dt.date(2019, 1, 18), dt.date(2019, 1, 25) ]
        XML_response = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><OptionExpireDateResponse>
                          <ExpirationDate><year>2019</year><month>1</month><day>18</day><expiryType>MONTHLY</expiryType></ExpirationDate>
                          <ExpirationDate><year>2019</year><month>1</month><day>25</day><expiryType>WEEKLY</expiryType></ExpirationDate>
                          </OptionExpireDateResponse>
                       '''
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_expire_date('AAPL', resp_format=None), response)
        self.assertTrue(MockOAuthSession().get.called)
        
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_expire_date('AAPL', resp_format='xml'), XML_response)
        self.assertTrue(MockOAuthSession().get.called)
