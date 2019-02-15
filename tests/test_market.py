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
           
        '''
           
        response = [{'symbol': 'MMM', 'description': '3M CO COM', 'type': 'EQUITY'}]
        XML_response =  r'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                            <LookupResponse>
                                <Data><symbol>MMM</symbol><description>3M CO COM</description><type>EQUITY</type></Data>
                            </LookupResponse>'''
        
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        # Test Get Quote returning python list
        self.assertEqual(mark.look_up_product('mmm'), response )
        self.assertTrue(MockOAuthSession().get.called)
        self.assertTrue(MockOAuthSession().fromstring.called)
        
        
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
                         
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_quote(['MMM']), response)
        self.assertTrue(MockOAuthSession().get.called)
        self.assertTrue(MockOAuthSession().fromstring.called)
                
        # test the assertion failure of detail_flag, requireEarningsDate, skipMiniOptionsCheck
        
        # Test log message if more than 25 quotes are requested
        # Generate 30 symbols; response should only be 25 symbols
        symbols = 30*['MMM']
        retn = 25*[response]
        MockOAuthSession().get().return_value = retn
        self.assertEqual(mark.get_quote(symbols), retn)
        self.assertTrue(MockOAuthSession().get.called)
        
        
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
                        
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_chains('AAPL', expiry_date=dt.date(2019, 2, 15)), response)
        self.assertTrue(MockOAuthSession().get.called)
        self.assertTrue(MockOAuthSession().fromstring.called)
            
            
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
                       
        MockOAuthSession().get().return_value = XML_response
        mark = market.ETradeMarket('abc123', 'xyz123', 'abctoken', 'xyzsecret', dev=False)
        self.assertEqual(mark.get_option_expire_date('AAPL'), response)
        self.assertTrue(MockOAuthSession().get.called)
        self.assertTrue(MockOAuthSession().fromstring.called)
