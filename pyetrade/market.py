#!/usr/bin/python3

"""Market - ETrade Market API V1

    Calling sequence to get all option chains for a particular month
    me = pyetrade.market.ETradeMarket(
                    consumer_key,
                    consumer_secret,
                    tokens['oauth_token'],
                    tokens['oauth_token_secret'],
                    dev = False)

    option_dates = me.get_option_expire_date('aapl')
    option_chains = me.get_option_chains('aapl')

    OR all inclusive:
        (option_dates,option_chains) = me.get_all_option_chains('aapl')
    TODO:
    * move logger into object under self.logger

"""

import logging
import xmltodict
from requests_oauthlib import OAuth1Session

LOGGER = logging.getLogger(__name__)


class ETradeMarket(object):
    """ETradeMarket"""

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
    ):
        """__init__(client_key, client_secret, resource_owner_key,
                    resource_owner_secret, dev=True)

            This is the object initialization routine, which simply
            sets the various variables to be used by the rest of the
            methods and constructs the OAuth1Session.

            param: client_key
            type: str
            description: etrade client key

            param: client_secret
            type: str
            description: etrade client secret

            param: resource_owner_key
            type: str
            description: OAuth authentication token key

            param: resource_owner_secret
            type: str
            description: OAuth authentication token secret

            param: dev
            type: boolean
            description: use the sandbox environment (True) or live (False)

        """
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.dev_environment = dev
        suffix = "apisb" if dev else "api"
        self.base_url = r"https://%s.etrade.com/v1/market/" % suffix
        self.session = OAuth1Session(
            self.client_key,
            self.client_secret,
            self.resource_owner_key,
            self.resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def __str__(self):
        ret = [
            "Use development environment: %s" % self.dev_environment,
            "base URL: %s" % self.base_url,
        ]
        return "\n".join(ret)

    def look_up_product(self, search_str: str, resp_format="xml") -> dict:
        """Look up product
           Args:
            search_str (str): full or partial name of the company. Note
                that the system extensivly abbreviates common words
                such as company, industry and systems and generally
                skips punctuation.
            resp_format (str): the api endpoint to hit (json or xml)
        """

        # api_url = self.base_url + "lookup/%s" % search_str
        api_url = "%slookup/%s" % (
            self.base_url,
            search_str if resp_format.lower() == "xml" else search_str + ".json",
        )
        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)
        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def get_quote(
        self,
        symbols,
        detail_flag=None,
        require_earnings_date=None,
        skip_mini_options_check=None,
        resp_format="xml",
    ) -> dict:
        """ get_quote(symbols, detail_flag=None, requireEarningsDate=None,
                      skipMiniOptionsCheck=None)

            Get quote data on all symbols provided in the list args.
            the eTrade API is limited to 25 requests per call. Issue
            warning if more than 25 are requested. Only process the first 25.

            param: skipMiniOptionsCheck
            type: True, False, None
            description: If value is true, no call is made to the service to check
            whether the symbol has mini options. If value is false or if the field
            is not specified, a service call is made to check if the symbol has mini
            options

            param: detailFlag
            type: enum
            required: optional
            description: Optional parameter specifying which details to
                return in the response. The field set for each possible
                value is listed in separate tables below. The possible
                values are:
                    * FUNDAMENTAL - Instrument fundamentals and latest
                        price
                    * INTRADAY - Performance for the current of most
                        recent trading day
                    * OPTIONS - Information on a given option offering
                    * WEEK_52 - 52-week high and low (highest high and
                        lowest low
                    * ALL (default) - All of the above information and
                        more
                    * MF_DETAIL - MutualFund structure gets displayed.

            param: symbols
            type: list
            required: true
            description: One or more symobols for equities or options, up to a
            maximum of  25 symbols.
                For equities, the symbol name alone, e.g. GOOGL.
                Symbols for options are more complex, consisting of six elements
                separated by colons, in this format:
                underlier:year:month:day:optionType:strikePrice
            """

        assert detail_flag in (
            "fundamental",
            "intraday",
            "options",
            "week_52",
            "all",
            "mf_detail",
            None,
        )
        assert require_earnings_date in (True, False, None)
        assert skip_mini_options_check in (True, False, None)
        assert isinstance(symbols, list or tuple)
        if len(symbols) > 25:
            LOGGER.warning(
                "get_quote asked for %d requests; only first 25 returned" % len(symbols)
            )

        args = list()
        if detail_flag is not None:
            args.append("detailflag=%s" % detail_flag.upper())
        if require_earnings_date:
            args.append("requireEarningsDate=true")
        if skip_mini_options_check is not None:
            args.append("skipMiniOptionsCheck=%s" % str(skip_mini_options_check))

        api_url = "%s%s%s" % (self.base_url, "quote/", ",".join(symbols[:25]))
        if resp_format.lower() == "json":
            api_url += ".json"
        if len(args):
            api_url += "?" + "&".join(args)
        LOGGER.debug(api_url)

        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def get_option_chains(
        self,
        underlier: str,
        expiry_date,
        skip_adjusted=None,
        chain_type=None,
        strike_price_near=None,
        no_of_strikes=None,
        option_category=None,
        price_type=None,
        resp_format="xml",
    ) -> dict:
        """ get_optionchains(underlier, expiry_date=None, skipAdjusted=None,
                             chainType=None, strikePriceNear=None, noOfStrikes=None,
                             optionCategory=None, priceType=None)

            Returns the option chain information for the requested expiry_date and
            chaintype in the desired format. This should be a list of dictionaries,
            one for each option chain.

            param: underlier
            description: market symbol

            param: chainType
            type: str
            description: put, call, or callput
            Default: callput

            param: priceType
            type: 'atmn', 'all', None
            description: The price type
            Default: ATNM

            param: expiry_date
            type: dt.date()
            description: contract expiration date; if expiry_date is None, then gets the
            expiration_date closest to today

            param: optionCategory
            type: 'standard', 'all', 'mini', None
            description: what type of option data to return
            Default: standard

            param: skipAdjusted
            type: bool
            description: Specifies whether to show (TRUE) or not show (FALSE) adjusted
                options, i.e., options that have undergone a change resulting
                in a modification of the option contract.

            Sample Request
            GET https://api.etrade.com/v1/market/optionchains?
            expiryDay=03&expiryMonth=04&expiryYear=2011
            &chainType=PUT&skipAdjusted=true&symbol=GOOGL

        """
        assert chain_type in ("put", "call", "callput", None)
        assert option_category in ("standard", "all", "mini", None)
        assert price_type in ("atmn", "all", None)
        assert skip_adjusted in (True, False, None)
        assert isinstance(resp_format, str)

        args = ["symbol=%s" % underlier]
        if expiry_date is not None:
            args.append(
                "expiryDay=%02d&expiryMonth=%02d&expiryYear=%04d"
                % (expiry_date.day, expiry_date.month, expiry_date.year)
            )
        if strike_price_near is not None:
            args.append("strikePriceNear=%0.2f" % strike_price_near)
        if chain_type is not None:
            args.append("chainType=%s" % chain_type.upper())
        if option_category is not None:
            args.append("optionCategory=%s" % option_category.upper())
        if price_type is not None:
            args.append("priceType=%s" % price_type.upper())
        if skip_adjusted is not None:
            args.append("skipAdjusted=%s" % str(skip_adjusted))
        if no_of_strikes is not None:
            args.append("noOfStrikes=%d" % no_of_strikes)
        api_url = "%s%s%s" % (
            self.base_url,
            "optionchains?" if resp_format.lower() == "xml" else "optionchains.json?",
            "&".join(args),
        )

        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(api_url)
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def get_option_expire_date(self, underlier: str, resp_format="xml") -> dict:
        """ get_option_expiry_dates(underlier)

            param: underlier
            description: market symbol

            https://api.etrade.com/v1/market/optionexpiredate?symbol={symbol}

            Sample Request
            GET https://api.etrade.com/v1/market/optionexpiredate?
               symbol=GOOG&expiryType=ALL
        """

        assert isinstance(resp_format, str)
        assert resp_format in ["xml", "json"]
        api_url = "%s%s" % (
            self.base_url,
            "optionexpiredate"
            if resp_format.lower() == "xml"
            else "optionexpiredate.json",
        )
        payload = {"symbol": underlier, "expiryType": "ALL"}
        LOGGER.debug(api_url)

        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()
