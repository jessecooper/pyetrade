#!/usr/bin/env python3
'''pyetrade authorization unit tests
   TODO:
       * Test request error'''

import unittest
from unittest.mock import patch
from pyetrade import accounts

class TestETradeAccounts(unittest.TestCase):
    '''TestEtradeAccounts Unit Test'''
    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_list_accounts(self, MockOAuthSession):
        '''test_list_accounts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text.return_value = r'<xml> returns </xml>'
        account = accounts.ETradeAccounts('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev JSON
        self.assertEqual(account.list_accounts(), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/accountlist.json')
                )
        # Test Prod JSON
        self.assertEqual(account.list_accounts(dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/accountlist.json')
                )
        # Test Dev XML
        self.assertEqual(account.list_accounts(resp_format='xml'), r'<xml> returns </xml>')
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get().text.called)
        self.assertTrue(MockOAuthSession().get.called)
    
    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_get_account_balance(self, MockOAuthSession):
        '''test_list_accounts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text.return_value = r'<xml> returns </xml>'
        account = accounts.ETradeAccounts('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev JSON
        self.assertEqual(account.get_account_balance(12345), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/accountbalance/12345.json')
                )
        # Test Prod JSON
        self.assertEqual(account.get_account_balance(12345, dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/accountbalance/12345.json')
                )
        # Test Dev XML
        self.assertEqual(account.get_account_balance(12345, resp_format='xml'), r'<xml> returns </xml>')
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get().text.called)
        self.assertTrue(MockOAuthSession().get.called)
        # TODO: called with to check url
