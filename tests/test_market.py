#!/usr/bin/env python3
"""pyetrade market unit tests
   TODO:
    * pyetrade.market fixture
"""
import datetime as dt
import unittest
from unittest.mock import patch
from pyetrade import market


# Mock out OAuth1Session
class TestETradeMarket(unittest.TestCase):
    """TestEtradeAccounts Unit Test"""

    @patch("pyetrade.market.OAuth1Session")
    def test_look_up_product(self, MockOAuthSession):
        """test_look_up_product(MockOAuthSession)
            param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session

           3 tests based on resp_format = (None,'xml')
           test exception raised when resp_format is something
           different from two choices
        """

        response = {"symbol": "MMM", "description": "3M CO COM", "type": "EQUITY"}
        XML_response = r"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                            <LookupResponse>
                                <Data><symbol>MMM</symbol>
                                <description>3M CO COM</description>
                                <type>EQUITY</type></Data>
                            </LookupResponse>"""
        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)
        # Test Get Quote returning python dict
        resp = mark.look_up_product("mmm")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Set Mock returns for resp_format=json
        MockOAuthSession().get().json.return_value = response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)
        # Test Get Quote returning python dict
        resp = mark.look_up_product("mmm", resp_format="json")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

    @patch("pyetrade.market.OAuth1Session")
    def test_get_quote(self, MockOAuthSession):
        """test_get_quote(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        """

        response = {
            "securityType": "EQ",
            "symbol": "MMM",
            "dateTimeUTC": 1546545180,
            "adjustedFlag": "false",
            "annualDividend": 0.0,
            "averageVolume": 3078683.0,
        }

        XML_response = r"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                            <QuoteResponse>
                                <QuoteData>
                                    <dateTime>14:53:00 EST 01-03-2019</dateTime>
                                    <dateTimeUTC>1546545180</dateTimeUTC>
                            <All>
                            <adjustedFlag>false</adjustedFlag>
                            <annualDividend>0.0</annualDividend>
                            <averageVolume>3078683</averageVolume></All>
                            <Product>
                            <securityType>EQ</securityType>
                            <symbol>MMM</symbol></Product>
                            </QuoteData></QuoteResponse>
                         """
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().text = XML_response
        MockOAuthSession().get().json.return_value = response

        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)

        # Test XML return
        resp = mark.get_quote(["MMM"])
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Test JSON return
        resp = mark.get_quote(["MMM"], resp_format="json")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Test list of symbols greater than 25
        resp = mark.get_quote(["MMM"]*26, resp_format="json")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Test list of symbols greater than 25
        resp = mark.get_quote(["MMM"] * 26, resp_format="json")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Test detail_flag, requireEarningsDate, skipMiniOptionsCheck
        resp = mark.get_quote(["MMM"], detail_flag="ALL", require_earnings_date=True,
                              skip_mini_options_check=True, resp_format="json")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/market/quote/MMM.json?detailflag=ALL&requireEarningsDate=true&skipMiniOptionsCheck=True"  # noqa: E501
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

        # test the assertion failure of detail_flag, requireEarningsDate,
        # skipMiniOptionsCheck

    @patch("pyetrade.market.OAuth1Session")
    def test_get_option_chains(self, MockOAuthSession):
        """test_get_optionexpiredate(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        """

        response = {"timeStamp": 1546546266, "bid": 41.55, "OptionGreeks": {"iv": 0.6716}}
        XML_response = r"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <OptionChainResponse><OptionPair><Call>
                           <timeStamp>1546546266</timeStamp><bid>41.55</bid>
                           <OptionGreeks><iv>0.435700</iv></OptionGreeks></Call>
                           </OptionPair></OptionChainResponse>
                        """

        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)
        resp = mark.get_option_chains("AAPL", expiry_date=dt.date(2019, 2, 15), resp_format="xml")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Set Mock returns for resp_format=xml and dev=True
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=True)
        resp = mark.get_option_chains("AAPL", expiry_date=dt.date(2019, 2, 15), resp_format="xml")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Set Mock returns for resp_format=xml
        MockOAuthSession().get().json.return_value = response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=True)
        resp = mark.get_option_chains("AAPL", expiry_date=dt.date(2019, 2, 15), resp_format="xml")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        # Set Mock returns for resp_format=json
        MockOAuthSession().get().json.return_value = response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)
        resp = mark.get_option_chains("AAPL", expiry_date=dt.date(2019, 2, 15),
                                      strike_price_near=100, chain_type="CALL", option_category="ALL",
                                      price_type="ALL", skip_adjusted=False, no_of_strikes=5, resp_format="json")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        MockOAuthSession().get.assert_called_with(
            "https://api.etrade.com/v1/market/optionchains.json?symbol=AAPL&expiryDay=15&expiryMonth=02&expiryYear=2019&strikePriceNear=100.00&chainType=CALL&optionCategory=ALL&priceType=ALL&skipAdjusted=False&noOfStrikes=5"  # noqa: E501
        )
        self.assertTrue(MockOAuthSession().get().json.called)
        self.assertTrue(MockOAuthSession().get.called)

        # test the assertion failure of chainType, optionCategory,
        # priceType, skipAdjusted

    @patch("pyetrade.market.OAuth1Session")
    def test_get_option_expire_date(self, MockOAuthSession):
        """test_get_optionexpiredate(MockOAuthSession)
           param: MockOAuthSession
           type: mock.MagicMock
           description: MagicMock of OAuth1Session
        """

        # response = [dt.date(2019, 1, 18), dt.date(2019, 1, 25)]
        XML_response = (
            r'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            r"<ExpirationDate></ExpirationDate>"
        )
        # Set Mock returns for resp_format=None
        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=False)
        resp = mark.get_option_expire_date("AAPL", resp_format="xml")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called

        MockOAuthSession().get().text = XML_response
        mark = market.ETradeMarket("abc123", "xyz123", "abctoken", "xyzsecret", dev=True)
        resp = mark.get_option_expire_date("AAPL", resp_format="xml")
        assert isinstance(resp, dict)
        assert MockOAuthSession().get.called
