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
        MockOAuthSession().get().text = r'<xml> returns </xml>'
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
        self.assertTrue(MockOAuthSession().get.called)
    
    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_get_account_balance(self, MockOAuthSession):
        '''test_get_account_balance(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text = r'<xml> returns </xml>'
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
        #MockOAuthSession().get.assert_called_with(
        #        ('https://etws.etrade.com/accounts/'
        #        'rest/accountbalance/12345')
        #        )

        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_get_account_positions(self, MockOAuthSession):
        '''test_get_account_positions(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text = r'<xml> returns </xml>'
        account = accounts.ETradeAccounts('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev JSON
        self.assertEqual(account.get_account_positions(12345), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/accountpositions/12345.json')
                )
        # Test Prod JSON
        self.assertEqual(account.get_account_positions(12345, dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/accountpositions/12345.json')
                )
        # Test Dev XML
        self.assertEqual(account.get_account_positions(12345, resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/accountpositions/12345')
                )
        self.assertEqual(account.get_account_positions(12345, dev=False, resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/accountpositions/12345')
                )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
    
    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_list_alerts(self, MockOAuthSession):
        '''test_list_alerts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text = r'<xml> returns </xml>'
        account = accounts.ETradeAccounts('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev JSON
        self.assertEqual(account.list_alerts(), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/alerts.json')
                )
        # Test Prod JSON
        self.assertEqual(account.list_alerts(dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/alerts.json')
                )
        # Test Dev XML
        self.assertEqual(account.list_alerts(resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/alerts')
                )
        self.assertEqual(account.list_alerts(dev=False, resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/alerts')
                )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_read_alert(self, MockOAuthSession):
        '''test_list_alerts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions'''
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text = r'<xml> returns </xml>'
        account = accounts.ETradeAccounts('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev JSON
        self.assertEqual(account.read_alert(1234), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/alerts/1234.json')
                )
        # Test Prod JSON
        self.assertEqual(account.read_alert(1234, dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/alerts/1234.json')
                )
        # Test Dev XML
        self.assertEqual(account.read_alert(1234, resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().get.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/alerts/1234')
                )
        self.assertEqual(account.read_alert(1234, dev=False, resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().get.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/alerts/1234')
                )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @patch('pyetrade.accounts.OAuth1Session')
    def test_delete_alert(self, MockOAuthSession):
        '''test_list_alerts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions'''
        # Set Mock returns
        MockOAuthSession().delete().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().delete().text = r'<xml> returns </xml>'
        account = accounts.ETradeAccounts('abc123', 'xyz123', 'abctoken', 'xyzsecret')
        # Test Dev JSON
        self.assertEqual(account.delete_alert(1234), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().delete.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/alerts/1234.json')
                )
        # Test Prod JSON
        self.assertEqual(account.delete_alert(1234, dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().delete.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/alerts/1234.json')
                )
        # Test Dev XML
        self.assertEqual(account.delete_alert(1234, resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().delete.assert_called_with(
                ('https://etwssandbox.etrade.com/accounts/'
                'sandbox/rest/alerts/1234')
                )
        self.assertEqual(account.delete_alert(1234, dev=False, resp_format='xml'), r'<xml> returns </xml>')
        MockOAuthSession().delete.assert_called_with(
                ('https://etws.etrade.com/accounts/'
                'rest/alerts/1234')
                )
        self.assertTrue(MockOAuthSession().delete().json.called)
        self.assertTrue(MockOAuthSession().delete.called)
