#!/usr/bin/env python3
'''pyetrade authorization unit tests
   TODO:
       * Test request error'''

import unittest
from unittest.mock import patch
from pyetrade import order, etrade_exception

class TestETradeOrder(unittest.TestCase):
    '''TestEtradeOrder Unit Test'''
    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_place_equity_order(self, MockOAuthSession):
        # Set Mock returns
        MockOAuthSession().post().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().post().text.return_value = r'<xml> returns </xml>'
        orders = order.ETradeOrder('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev JSON
        #self.assertEqual(orders.place_equity_order(), "{'account': 'abc123'}") 
        with self.assertRaises(etrade_exception.OrderException):
            orders.place_equity_order()
        # Test Prod JSON
        #self.assertEqual(orders.place_equity_order(dev=False), "{'account': 'abc123'}") 
        # Test Dev XML
        #self.assertEqual(orders.place_equity_order(resp_format='xml'), r'<xml> returns </xml>') 
        #self.assertTrue(MockOAuthSession().get().json.called) 
        #self.assertTrue(MockOAuthSession().get().text.called) 
        #self.assertTrue(MockOAuthSession().get.called) 
        
