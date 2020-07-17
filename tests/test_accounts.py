#!/usr/bin/env python3
"""pyetrade authorization unit tests
   TODO:
       * Test request error"""

import pytest
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
        result = account.get_account_balance("12345", resp_format="xml")
        self.assertTrue(isinstance(result, dict))
        # Test Dev JSON
        result = account.get_account_balance("12345", resp_format="json")
        self.assertTrue(isinstance(result, dict))
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345/balance.json",
            params={"instType": "BROKERAGE", "realTimeNAV": True},
        )
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test Prod JSON
        result = account.get_account_balance("12345", resp_format="json")
        self.assertTrue(isinstance(result, dict))
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345/balance.json",
            params={"instType": "BROKERAGE", "realTimeNAV": True},
        )
        # xml prod
        result = account.get_account_balance("12345", resp_format="xml")
        self.assertTrue(isinstance(result, dict))

        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345/balance",
            params={"instType": "BROKERAGE", "realTimeNAV": True},
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
        # Test Dev
        result = account.get_account_portfolio("12345")
        self.assertTrue(isinstance(result, dict))
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345/portfolio", params={}
        )
        result = account.get_account_portfolio("12345", resp_format="json")
        self.assertTrue(isinstance(result, dict))
        # Test Prod
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        result = account.get_account_portfolio("12345")
        self.assertTrue(isinstance(result, dict))
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345/portfolio", params={}
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
        result = account.get_account_portfolio("12345", resp_format="xml")
        self.assertTrue(isinstance(result, dict))

    # Mock out OAuth1Session
    @pytest.mark.skip(reason="v0 test")
    @patch("pyetrade.accounts.OAuth1Session")
    def test_list_alerts(self, MockOAuthSession):
        """test_list_alerts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text = r"<xml> returns </xml>"
        account = accounts.ETradeAccounts("abc123", "xyz123", "abctoken", "xyzsecret")
        # Test Dev JSON
        self.assertEqual(account.list_alerts(), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/" "sandbox/rest/alerts.json")
        )
        # Test Prod JSON
        self.assertEqual(account.list_alerts(dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/" "rest/alerts.json")
        )
        # Test Dev XML
        self.assertEqual(
            account.list_alerts(resp_format="xml"), r"<xml> returns </xml>"
        )
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/" "sandbox/rest/alerts")
        )
        self.assertEqual(
            account.list_alerts(dev=False, resp_format="xml"), r"<xml> returns </xml>"
        )
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/" "rest/alerts")
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @pytest.mark.skip(reason="v0 test")
    @patch("pyetrade.accounts.OAuth1Session")
    def test_read_alert(self, MockOAuthSession):
        """test_list_alerts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().get().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().get().text = r"<xml> returns </xml>"
        account = accounts.ETradeAccounts("abc123", "xyz123", "abctoken", "xyzsecret")
        # Test Dev JSON
        self.assertEqual(account.read_alert(1234), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/" "sandbox/rest/alerts/1234.json")
        )
        # Test Prod JSON
        self.assertEqual(account.read_alert(1234, dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/" "rest/alerts/1234.json")
        )
        # Test Dev XML
        self.assertEqual(
            account.read_alert(1234, resp_format="xml"), r"<xml> returns </xml>"
        )
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/" "sandbox/rest/alerts/1234")
        )
        self.assertEqual(
            account.read_alert(1234, dev=False, resp_format="xml"),
            r"<xml> returns </xml>",
        )
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/" "rest/alerts/1234")
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

    # Mock out OAuth1Session
    @pytest.mark.skip(reason="v0 test")
    @patch("pyetrade.accounts.OAuth1Session")
    def test_delete_alert(self, MockOAuthSession):
        """test_list_alerts(MockOAuthSession) -> None
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock object for OAuth1Sessions"""
        # Set Mock returns
        MockOAuthSession().delete().json.return_value = "{'account': 'abc123'}"
        MockOAuthSession().delete().text = r"<xml> returns </xml>"
        account = accounts.ETradeAccounts("abc123", "xyz123", "abctoken", "xyzsecret")
        # Test Dev JSON
        self.assertEqual(account.delete_alert(1234), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().delete.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/" "sandbox/rest/alerts/1234.json")
        )
        # Test Prod JSON
        self.assertEqual(account.delete_alert(1234, dev=False), "{'account': 'abc123'}")
        # Test API URL
        MockOAuthSession().delete.assert_called_with(
            ("https://api.etrade.com/v1/accounts/" "rest/alerts/1234.json")
        )
        # Test Dev XML
        self.assertEqual(
            account.delete_alert(1234, resp_format="xml"), r"<xml> returns </xml>"
        )
        MockOAuthSession().delete.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/" "sandbox/rest/alerts/1234")
        )
        self.assertEqual(
            account.delete_alert(1234, dev=False, resp_format="xml"),
            r"<xml> returns </xml>",
        )
        MockOAuthSession().delete.assert_called_with(
            ("https://api.etrade.com/v1/accounts/" "rest/alerts/1234")
        )
        self.assertTrue(MockOAuthSession().delete().json.called)
        self.assertTrue(MockOAuthSession().delete.called)

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
        # Test Dev JSON
        self.assertEqual(
            account.list_transactions(12345, resp_format="json"),
            "{'transaction': 'abc123'}",
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/12345/transactions.json"), params={},
        )

        # Test Dev XML
        self.assertEqual(
            dict(account.list_transactions(12345, resp_format="xml")),
            {"xml": "returns"},
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts/12345/transactions"), params={},
        )
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test Prod JSON
        self.assertEqual(
            account.list_transactions(12345, resp_format="json"),
            "{'transaction': 'abc123'}",
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/12345/transactions.json"), params={},
        )
        # Test Prod XML
        self.assertEqual(
            dict(account.list_transactions(12345, resp_format="xml")),
            {"xml": "returns"},
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/12345/transactions"), params={}
        )
        # Test optional_args
        self.assertEqual(
            account.list_transactions(12345, group="WITHDRAWALS", resp_format="json"),
            "{'transaction': 'abc123'}",
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
            account.list_transaction_details(12345, 67890, resp_format="json"),
            "{'transaction': 'abc123'}",
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://apisb.etrade.com/v1/accounts" "/12345/transactions.json/67890"),
            params={},
        )
        # Test Dev XML
        self.assertEqual(
            dict(account.list_transaction_details(12345, 67890, resp_format="xml")),
            {"xml": "returns"},
        )
        MockOAuthSession().get.assert_called_with(
            "https://apisb.etrade.com/v1/accounts/12345/transactions/67890", params={},
        )
        account = accounts.ETradeAccounts(
            "abc123", "xyz123", "abctoken", "xyzsecret", dev=False
        )
        # Test Prod JSON
        self.assertEqual(
            account.list_transaction_details(12345, 67890, resp_format="json"),
            "{'transaction': 'abc123'}",
        )
        # Test API URL
        MockOAuthSession().get.assert_called_with(
            ("https://api.etrade.com/v1/accounts/12345/transactions.json/67890"),
            params={},
        )
        # Test Prod XML
        self.assertEqual(
            dict(account.list_transaction_details(12345, 67890, resp_format="xml")),
            {"xml": "returns"},
        )
        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/accounts/12345/transactions/67890", params={},
        )

        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)
