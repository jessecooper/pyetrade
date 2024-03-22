#!/usr/bin/env python3
"""pyetrade authorization unit tests
   TODO:
       * Test request error"""

import unittest
from unittest.mock import patch
from pyetrade import accounts


class TestETradeAccounts(unittest.TestCase):
    """TestEtradeAccounts Unit Test"""

    # Mock out OAuth1Session
    @patch("pyetrade.accounts.OAuth1Session")
    def test_list_accounts(self, MockOAuthSession):
        """test_list_accounts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text = r"<xml> returns </xml>"
        account = accounts.ETradeAccounts("abc123", "xyz123", "abctoken", "xyzsecret")
        # Test Dev JSON
        self.assertEqual(
            account.list_accounts(resp_format="json"), "{'account': 'abc123'}"
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/list.json")
        )
        # Test Dev XML
        result = account.list_accounts(resp_format="xml")
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(MockOAuthSession().get.called)

        # Test Prod JSON
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        self.assertEqual(
            account.list_accounts(resp_format="json"), "{'account': 'abc123'}"
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/list.json")
        )
        # Test XML
        result = account.list_accounts(resp_format="xml")
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @patch("pyetrade.accounts.OAuth1Session")
    def test_get_account_balance(self, MockOAuthSession):
        """test_get_account_balance(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = {"account": "abc123"}
        MockOAuthSession().get().text = r"<xml> returns </xml>"
        account = accounts.ETradeAccounts("abc123", "xyz123", "abctoken", "xyzsecret")
        # Test Dev XML
        result = account.get_account_balance("12345abcd", resp_format="xml")
        self.assertTrue(isinstance(result, dict))
        # Test Dev JSON
        result = account.get_account_balance("12345abcd", resp_format="json")
        self.assertTrue(isinstance(result, dict))
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345abcd/balance.json",
            params={"instType": "BROKERAGE", "realTimeNAV": True},
        )
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test Prod JSON
        result = account.get_account_balance("12345abcd", resp_format="json")
        self.assertTrue(isinstance(result, dict))
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/balance.json",
            params={"instType": "BROKERAGE", "realTimeNAV": True},
        )
        # xml prod
        result = account.get_account_balance("12345abcd", resp_format="xml")
        self.assertTrue(isinstance(result, dict))

        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/balance",
            params={"instType": "BROKERAGE", "realTimeNAV": True},
        )

        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

        # Test API URL
        result = account.get_account_balance("12345abcd", account_type="TRUST", resp_format="json")
        self.assertTrue(isinstance(result, dict))

        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/balance.json",
            params={"realTimeNAV": True, "instType": "BROKERAGE", "accountType": "TRUST"},
        )

        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @patch("pyetrade.accounts.OAuth1Session")
    def test_get_account_portfolio(self, MockOAuthSession):
        """test_get_account_positions(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = {"account": "abc123"}
        MockOAuthSession().get().text = r"<xml> returns </xml>"

        account = accounts.ETradeAccounts("abc123", "xyz123", "abctoken", "xyzsecret")
        default_params = {
            'count': 50,
            'sortBy': None,
            'sortOrder': 'DESC',
            'pageNumber': None,
            'marketSession': 'REGULAR',
            'totalsRequired': False,
            'lotsRequired': False,
            'view': 'QUICK'
        }

        # Test Dev
        result = account.get_account_portfolio("12345abcd")
        self.assertTrue(isinstance(result, dict))

        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345abcd/portfolio", params=default_params
        )
        result = account.get_account_portfolio("12345abcd", resp_format="json")
        self.assertTrue(isinstance(result, dict))

        # Test Prod
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        result = account.get_account_portfolio("12345abcd")
        self.assertTrue(isinstance(result, dict))

        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/portfolio", params=default_params
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        result = account.get_account_portfolio("12345abcd", resp_format="xml")
        self.assertTrue(isinstance(result, dict))

    # Mock out OAuth1Session
    @patch("pyetrade.accounts.OAuth1Session")
    def test_list_transactions(self, MockOAuthSession):
        """test_list_transactions(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'transaction': 'abc123'}"
        MockOAuthSession().get().text = r"<xml> returns </xml>"

        account = accounts.ETradeAccounts("abc123", "xyz123", "abctoken", "xyzsecret")
        default_params = {'startDate': None, 'endDate': None, 'sortOrder': 'DESC', 'marker': None, 'count': 50}

        # Test Dev JSON
        self.assertEqual(
            account.list_transactions('12345abcd', resp_format="json"), "{'transaction': 'abc123'}"

        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345abcd/transactions.json", params=default_params,
        )
        # Test Dev XML
        self.assertEqual(
            dict(account.list_transactions('12345abcd', resp_format="xml")), {"xml": "returns"},
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345abcd/transactions", params=default_params,
        )
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test Prod JSON
        self.assertEqual(
            account.list_transactions('12345abcd', resp_format="json"), "{'transaction': 'abc123'}",
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/transactions.json", params=default_params,
        )
        # Test Prod XML
        self.assertEqual(
            dict(account.list_transactions('12345abcd', resp_format="xml")), {"xml": "returns"},
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/transactions", params=default_params
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @patch("pyetrade.accounts.OAuth1Session")
    def test_list_transaction_details(self, MockOAuthSession):
        """test_get_transaction_details(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'transaction': 'abc123'}"
        MockOAuthSession().get().text = r"<xml> returns </xml>"
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=True
        )
        # Test Dev JSON
        self.assertEqual(
            account.list_transaction_details('12345abcd', 67890, resp_format="json"),
            "{'transaction': 'abc123'}",
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts" "/12345abcd/transactions.json/67890", params={},
        )
        # Test Dev XML
        self.assertEqual(
            dict(account.list_transaction_details('12345abcd', 67890, resp_format="xml")),
            {"xml": "returns"},
        )
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345abcd/transactions/67890", params={},
        )
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test Prod JSON
        self.assertEqual(
            account.list_transaction_details('12345abcd', 67890, resp_format="json"),
            "{'transaction': 'abc123'}",
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/transactions.json/67890", params={},
        )
        # Test Prod XML
        self.assertEqual(
            dict(account.list_transaction_details('12345abcd', 67890, resp_format="xml")),
            {"xml": "returns"},
        )
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345abcd/transactions/67890", params={},
        )

        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
