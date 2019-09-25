#!/usr/bin/python3

"""Accounts - ETrade Accounts API
   Calls
   TODO:
       * list transactions APIv1
       * list transaction details APIv1
       * Fix init doc string
       * Check request response for error"""

import logging
import jxmlease
from requests_oauthlib import OAuth1Session

# Set up logging
LOGGER = logging.getLogger(__name__)


class ETradeAccounts(object):
    """ETradeAccounts:"""

    def __init__(
        self, client_key, client_secret, resource_owner_key, resource_owner_secret
    ):
        """__init_()
           """
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.base_url_prod = r"https://api.etrade.com/v1/accounts"
        self.base_url_dev = r"https://apisb.etrade.com/v1/accounts"
        self.session = OAuth1Session(
            self.client_key,
            self.client_secret,
            self.resource_owner_key,
            self.resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_accounts(self, dev=True, resp_format="json"):
        """list_account(dev, resp_format)
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

        if dev:
            if resp_format == "json":
                uri = r"list"
                api_url = "%s/%s.%s" % (self.base_url_dev, uri, resp_format)
            elif resp_format == "xml":
                uri = r"list"
                api_url = "%s/%s" % (self.base_url_dev, uri)
        else:
            if resp_format == "json":
                uri = r"list"
                api_url = "%s/%s.%s" % (self.base_url_prod, uri, resp_format)
            elif resp_format == "xml":
                uri = r"list"
                api_url = "%s/%s" % (self.base_url_prod, uri)

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        else:
            return jxmlease.parse(req.text)

    def get_account_balance(
        self,
        account_id,
        account_type=None,
        real_time=True,
        dev=True,
        resp_format="json",
    ):
        """get_account_balance(dev, resp_format)
           param: account_id
           type: int
           required: true
           description: Numeric account id
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

        uri = "balance"
        payload = {"realTimeNAV": real_time, "instType": "BROKERAGE"}
        if account_type:
            payload["accountType"] = account_type

        if dev:
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_dev,
                    account_id,
                    uri,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_dev, account_id, uri)
        else:
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_prod,
                    account_id,
                    uri,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_prod, account_id, uri)
        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        else:
            return jxmlease.parse(req.text)

    def get_account_positions(self, account_id, dev=True, resp_format="json"):
        """get_account_positions(dev, account_id, resp_format) -> resp
           param: account_id
           type: string
           required: true
           description: account id key
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

        if dev:
            api_url = self.base_url_dev
        else:
            api_url = self.base_url_prod

        api_url += "/" + account_id + "/portfolio"
        if resp_format == "json":
            api_url += ".json"

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return jxmlease.parse(req.text)

    def list_alerts(self, dev=True, resp_format="json"):
        """list_alerts(dev, resp_format) -> resp
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

        if dev:
            uri = r"accounts/sandbox/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s.%s" % (self.base_url_dev, uri, resp_format)
            elif resp_format == "xml":
                api_url = "%s/%s" % (self.base_url_dev, uri)

        else:
            uri = r"accounts/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s.%s" % (self.base_url_prod, uri, resp_format)
            elif resp_format == "xml":
                api_url = "%s/%s" % (self.base_url_prod, uri)

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return req.text

    def read_alert(self, alert_id, dev=True, resp_format="json"):
        """read_alert(alert_id, dev, resp_format) -> resp
           param: alert_id
           type: int
           description: Numaric alert ID
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

        if dev:
            uri = r"accounts/sandbox/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_dev,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_dev, uri, alert_id)

        else:
            uri = r"accounts/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_prod,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_prod, uri, alert_id)

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return req.text

    def delete_alert(self, alert_id, dev=True, resp_format="json"):
        """delete_alert(alert_id, dev, resp_format) -> resp
           param: alert_id
           type: int
           description: Numaric alert ID
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

        if dev:
            uri = r"accounts/sandbox/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_dev,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_dev, uri, alert_id)

        else:
            uri = r"accounts/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_prod,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_prod, uri, alert_id)

        LOGGER.debug(api_url)
        req = self.session.delete(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return req.text

    def get_transaction_history(
        self,
        account_id,
        dev=True,
        group="ALL",
        asset_type="ALL",
        transaction_type="ALL",
        ticker_symbol="ALL",
        resp_format="json",
        **kwargs
    ):
        """get_transaction_history(account_id, dev, resp_format) -> resp
           param: account_id
           type: int
           required: true
           description: Numeric account ID
           param: group
           type: string
           default: 'ALL'
           description: Possible values are: DEPOSITS, WITHDRAWALS, TRADES.
           param: asset_type
           type: string
           default: 'ALL'
           description: Only allowed if group is TRADES. Possible values are:
                EQ (equities), OPTN (options), MMF (money market funds),
                MF (mutual funds), BOND (bonds). To retrieve all types,
                use ALL or omit this parameter.
           param: transaction_type
           type: string
           default: 'ALL'
           description: Transaction type(s) to include, e.g., check, deposit,
                fee, dividend, etc. A list of types is provided in documentation
           param: ticker_symbol
           type: string
           default: 'ALL'
           description: Only allowed if group is TRADES. A single market symbol,
                e.g., GOOG.
           param: marker
           type: str
           description: Specify the desired starting point of the set
                of items to return. Used for paging.
           param: count
           type: int
           description: The number of orders to return in a response.
                The default is 25. Used for paging.
           description: see ETrade API docs"""

        # add each optional argument not equal to 'ALL' to the uri
        optional_args = [group, asset_type, transaction_type, ticker_symbol]
        optional_uri = ""
        for optional_arg in optional_args:
            if optional_arg.upper() != "ALL":
                optional_uri = "%s/%s" % (optional_uri, optional_arg)
        # Set Env
        if dev:
            # assemble the following:
            # self.base_url_dev: https://etws.etrade.com
            # uri:               /accounts/rest
            # account_id:        /{accountId}
            # format string:     /transactions
            # if not 'ALL' args:
            #   group:              /{Group}
            #   asset_type          /{AssetType}
            #   transaction_type:   /{TransactionType}
            #   ticker_symbol:      /{TickerSymbol}
            # resp_format:       {.json}
            # payload:           kwargs
            #
            uri = r"accounts/sandbox/rest"
            if resp_format == "json":
                api_url = "%s/%s/%s/transactions%s.%s" % (
                    self.base_url_dev,
                    uri,
                    account_id,
                    optional_uri,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s/transactions%s" % (
                    self.base_url_dev,
                    uri,
                    account_id,
                    optional_uri,
                )
        else:
            uri = r"accounts/rest"
            if resp_format == "json":
                api_url = "%s/%s/%s/transactions%s.%s" % (
                    self.base_url_prod,
                    uri,
                    account_id,
                    optional_uri,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s/transactions%s" % (
                    self.base_url_prod,
                    uri,
                    account_id,
                    optional_uri,
                )

        # Build Payload
        payload = kwargs
        LOGGER.debug("payload: %s", payload)

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return req.text

    def get_transaction_details(
        self, account_id, transaction_id, dev=True, resp_format="json", **kwargs
    ):
        """get_transaction_details(account_id, transaction_id, dev, resp_format) -> resp
           param: account_id
           type: int
           required: true
           description: Numeric account ID
           param: transaction_id
           type: int
           required: true
           description: Numeric transaction ID"""

        # Set Env
        if dev:
            uri = r"accounts/sandbox/rest"
            if resp_format == "json":
                api_url = "%s/%s/%s/transactions/%s.%s" % (
                    self.base_url_dev,
                    uri,
                    account_id,
                    transaction_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s/transactions/%s" % (
                    self.base_url_dev,
                    uri,
                    account_id,
                    transaction_id,
                )
        else:
            uri = r"accounts/rest"
            if resp_format == "json":
                api_url = "%s/%s/%s/transactions/%s.%s" % (
                    self.base_url_prod,
                    uri,
                    account_id,
                    transaction_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s/transactions/%s" % (
                    self.base_url_prod,
                    uri,
                    account_id,
                    transaction_id,
                )

        # Build Payload
        payload = kwargs
        LOGGER.debug("payload: %s", payload)

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return req.text
