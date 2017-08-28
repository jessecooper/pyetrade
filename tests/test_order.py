#!/usr/bin/env python3
'''pyetrade authorization unit tests
   TODO:
       * Test request error
       * Test API URL'''

import unittest
from unittest.mock import patch
from pyetrade import order, etrade_exception

class TestETradeOrder(unittest.TestCase):
    '''TestEtradeOrder Unit Test'''
    @patch('pyetrade.order.OAuth1Session')
    def test_list_orders(self, MockOAuthSession):
        '''test_place_equity_order(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'accountId': '12345'}"
        MockOAuthSession().get().text = r'<xml> returns </xml>'
        orders = order.ETradeOrder('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev buy order equity
        self.assertEqual(orders.list_orders('12345'), "{'accountId': '12345'}")
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        # Test Prod buy order equity
        self.assertEqual(orders.list_orders('12345', dev=False), "{'accountId': '12345'}")
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        self.assertEqual(orders.list_orders('12345', dev=False, resp_format='xml'), r'<xml> returns </xml>')
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
    # Mock out OAuth1Session
    @patch('pyetrade.order.OAuth1Session')
    def test_place_equity_order(self, MockOAuthSession):
        '''test_place_equity_order(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session'''
        # Set Mock returns
        MockOAuthSession().post().json.return_value = "{'accountId': '12345'}"
        MockOAuthSession().post().text = r'<xml> returns </xml>'
        orders = order.ETradeOrder('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev buy order equity
        self.assertEqual(orders.place_equity_order(accountId=12345,
                                                   symbol='ABC',
                                                   orderAction='BUY',
                                                   clientOrderId='1a2b3c',
                                                   priceType='MARKET',
                                                   quantity=100,
                                                   orderTerm='GOOD_UNTIL_CANCEL',
                                                   marketSession='REGULAR'), "{'accountId': '12345'}")
        self.assertTrue(MockOAuthSession().post().json.called)
        self.assertTrue(MockOAuthSession().post.called)
        # Test prod buy order equity
        self.assertEqual(orders.place_equity_order(dev=False,
                                                   accountId=12345,
                                                   symbol='ABC',
                                                   orderAction='BUY',
                                                   clientOrderId='1a2b3c',
                                                   priceType='MARKET',
                                                   quantity=100,
                                                   orderTerm='GOOD_UNTIL_CANCEL',
                                                   marketSession='REGULAR'), "{'accountId': '12345'}")
        self.assertTrue(MockOAuthSession().post().json.called)
        self.assertTrue(MockOAuthSession().post.called)
        # Test prod buy order equity
        self.assertEqual(orders.place_equity_order(dev=False,
                                                   resp_format='text',
                                                   accountId=12345,
                                                   symbol='ABC',
                                                   orderAction='BUY',
                                                   clientOrderId='1a2b3c',
                                                   priceType='MARKET',
                                                   quantity=100,
                                                   orderTerm='GOOD_UNTIL_CANCEL',
                                                   marketSession='REGULAR'), "<xml> returns </xml>")
        self.assertTrue(MockOAuthSession().post().json.called)
        self.assertTrue(MockOAuthSession().post.called)

    @patch('pyetrade.order.OAuth1Session')
    def test_place_equity_order_exception(self, MockOAuthSession):
        '''test_place_equity_order_exception(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session'''
        orders = order.ETradeOrder('abc123', 'xyz123', 'abctoken', 'xyzsecret')

        # Test exception class
        with self.assertRaises(etrade_exception.OrderException):
            orders.place_equity_order()
        # Test STOP
        with self.assertRaises(etrade_exception.OrderException):
            orders.place_equity_order(accountId=12345,
                                      symbol='ABC',
                                      orderAction='BUY',
                                      clientOrderId='1a2b3c',
                                      priceType='STOP',
                                      quantity=100,
                                      orderTerm='GOOD_UNTIL_CANCEL',
                                      marketSession='REGULAR')
        #Test LIMIT
        with self.assertRaises(etrade_exception.OrderException):
            orders.place_equity_order(accountId=12345,
                                      symbol='ABC',
                                      orderAction='BUY',
                                      clientOrderId='1a2b3c',
                                      priceType='LIMIT',
                                      quantity=100,
                                      orderTerm='GOOD_UNTIL_CANCEL',
                                      marketSession='REGULAR')
        #Test STOP_LIMIT
        with self.assertRaises(etrade_exception.OrderException):
            orders.place_equity_order(accountId=12345,
                                      symbol='ABC',
                                      orderAction='BUY',
                                      clientOrderId='1a2b3c',
                                      priceType='STOP_LIMIT',
                                      quantity=100,
                                      orderTerm='GOOD_UNTIL_CANCEL',
                                      marketSession='REGULAR')
        # Test Prod JSON
        #self.assertEqual(orders.place_equity_order(dev=False), "{'account': 'abc123'}")
        # Test Dev XML
        #self.assertEqual(orders.place_equity_order(resp_format='xml'), r'<xml> returns </xml>')
        #self.assertTrue(MockOAuthSession().get().text.called)
        
