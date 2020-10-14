"""Market - ETrade Market API V1

    TODO:
    * move logger into object under self.logger

"""

import logging
import xmltodict
from requests_oauthlib import OAuth1Session

LOGGER = logging.getLogger(__name__)


class ETradeMarket(object):
    """:description: Performs Market functions

       :param client_key: Client key provided by Etrade
       :type client_key: str, required
       :param client_secret: Client secret provided by Etrade
       :type client_secret: str, required
       :param resource_owner_key: Resource key from :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_key: str, required
       :param resource_owner_secret: Resource secret from
              :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_secret: str, required
       :param dev: Defines Sandboxi (True) or Live (False) ETrade, defaults to True
       :type dev: bool, optional
       :EtradeRef: https://apisb.etrade.com/docs/api/market/api-quote-v1.html

    """

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
    ):
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
        """:description: Performs a look up product

           :param search_str: Full or partial name of the company.
           :type search_str: str, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: Product lookup
           :rtype: ``xml`` or ``json`` as defined by ``resp_format``
           :Note: Etrade abbreviates common words such as company, industry and systems
                  and generally skips punctuation.
           :EtradeRef:
                  https://apisb.etrade.com/docs/api/market/api-market-v1.html#/definition/Lookup

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
        """:description: Get quote data on symbols provided in the list args.

           :param symbols: Symbols in list args format. Limit 25.
           :type symbols: list[], required
           :param detail_flag: Market fields returned from a quote request, defaults to None
           :type detail_flag: enum, optional
           :param require_earnings_date: Provides Earnings date if True, defaults to None
           :type require_earnings_date: str, optional
           :param skip_mini_options_check: Skips mini options check if True, defaults to None
           :type skip_mini_options_check: str, optional
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: Returns quote data on symbols provided
           :rtype: xml or json based on ``resp_format``
           :symbols values:
               * Limited to 25. If exceeded, first 25 will be processed with warnings
               * Equities format - ``symbol`` name sufficient, e.g. GOOGL.
               * Options format - ``underlier:year:month:day:optionType:strikePrice``
           :detailflag values:
               * fundamental - Instrument fundamentals and latest price
               * intraday - Performance for the current of most recent trading day
               * options - Information on a given option offering
               * week_52 - 52-week high and low (highest high and lowest low)
               * mf_detail - MutualFund structure gets displayed
               * all (default) - All of the above information and more
               * None - Defaults to all.
           :skipMiniOptionsCheck values:
               * True - Call is NOT made to check whether the symbol has mini options
               * False - Call is made to check whether the symbol has mini options
               * None - Call is made to check whether the symbol has mini options (default)
           :EtradeRef: https://apisb.etrade.com/docs/api/market/api-quote-v1.html

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
        """:description: Returns the option chain information for the
                         requested expiry_date and chaintype in the desired format.
                         This should be a list of dictionaries,
                         one for each option chain.

           :param underlier: Market Symbol
           :type underlier: str, required
           :param expiry_date: Contract expiration date, None produces closest to today
           :type expiry_date: datetime.date(year, month, day), optional
           :param skip_adjusted: Specifies whether to show (True) or not show (False) adjusted
                                 options, defaults to True
           :type skip_adjusted: str, optional
           :param chain_type: Type of option chain, defaults to callput
           :type chain_type: str, optional
           :param strike_price_near: Optionchains fetched will have strike price close to this value
           :type strike_price_near: int, optional
           :param no_of_strikes: Indicates number of strikes for which the optionchain
                                 needs to be fetched, defaults to None
           :type no_of_strikes: int, optional
           :param option_category: The option category, defaults to ``standard``
           :type option_category: str, optional
           :param price_type: The price type, defaults to ``atnm``
           :type price_type: str, optional
           :param resp_format: Desired Response format, defaults to ``xml``
           :type  resp_format: str, optional
           :return: Returns list of option chains for a specific underlying instrument
           :rtype: xml or json based on ``resp_format``
           :chain_type values:
               * put
               * call
               * callput (default)
           :option_category values:
               * standard (default)
               * all
               * mini
           :price_type values:
               * atnm
               * all
           :sampleURL: https://api.etrade.com/v1/market/optionchains?expiryDay=03&expiryMonth=04&expiryYear=2011&chainType=PUT&skipAdjusted=true&symbol=GOOGL
           :EtradeRef: https://apisb.etrade.com/docs/api/market/api-market-v1.html

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
        """:description: Returns a list of dates suitable for structuring an option table display

           :param underlier: Market Symbol
           :type underlier: str, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: Returns expiry of options for symbol
           :rtype: xml or json based on ``resp_format``
           :sampleURL: https://api.etrade.com/v1/market/optionexpiredate?symbol=GOOG&expiryType=ALL
           :EtradeRef: https://apisb.etrade.com/docs/api/market/api-market-v1.html

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
