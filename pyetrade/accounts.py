"""Accounts - ETrade Accounts API
   Calls
   TODO:
       * Fix init doc string
       * Check request response for error"""

import logging
import xmltodict
from requests_oauthlib import OAuth1Session

# Set up logging
LOGGER = logging.getLogger(__name__)


class ETradeAccounts(object):
    """ETradeAccounts:"""

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
    ):
        """__init_()
           """
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        suffix = "apisb" if dev else "api"
        self.base_url = r"https://%s.etrade.com/v1/accounts" % suffix
        # self.base_url_prod = r"https://api.etrade.com/v1/accounts"
        # self.base_url_dev = r"https://apisb.etrade.com/v1/accounts"
        self.session = OAuth1Session(
            self.client_key,
            self.client_secret,
            self.resource_owner_key,
            self.resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_accounts(self, resp_format="xml") -> dict:
        """list_account(dev, resp_format)
           param: resp_format
           description: Response format
        """

        api_url = "%s/list%s" % (
            self.base_url,
            ".json" if resp_format == "json" else "",
        )

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def get_account_balance(
        self, account_id_key: str, account_type=None, real_time=True, resp_format="xml"
    ) -> dict:
        """get_account_balance(dev, resp_format)
           param: account_id
           required: true
           description: Numeric account id
           param: resp_format
           description: Response format
        """

        api_url = "%s/%s/balance%s" % (
            self.base_url,
            account_id_key,
            ".json" if resp_format == "json" else "",
        )
        payload = {"realTimeNAV": real_time, "instType": "BROKERAGE"}
        if account_type:
            payload["accountType"] = account_type

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def get_account_portfolio(
        self, account_id_key: str, resp_format="xml", **kwargs
    ) -> dict:
        """get_account_portfolio(dev, account_id, esp_format) -> resp
           param: account_id_key
           required: true
           description: account id key
           param: resp_format
           description: Response format
           param: kwargs
           description:
           https://apisb.etrade.com/docs/api/account/api-portfolio-v1.html
           """

        api_url = "%s/%s/portfolio%s" % (
            self.base_url,
            account_id_key,
            ".json" if resp_format == "json" else "",
        )

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=kwargs)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def list_transactions(
        self, account_id_key: str, resp_format="xml", **kwargs
    ) -> dict:
        """list_transactions(account_id_key, resp_format) -> resp
           param: account_id_key
           required: true
           description: Numeric account ID
           param: kwargs
           description: see etrade docs for details
        """

        api_url = "%s/%s/transactions%s" % (
            self.base_url,
            account_id_key,
            ".json" if resp_format == "json" else "",
        )

        # Build Payload
        payload = kwargs
        LOGGER.debug("payload: %s", payload)

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def list_transaction_details(
        self, account_id_key: str, transaction_id: int, resp_format="xml", **kwargs
    ) -> dict:
        """get_transaction_details(account_id, transaction_id, dev, resp_format) -> resp
           param: account_id_key
           type: str
           required: true
           description: Numeric account ID
           param: transaction_id
           type: int
           required: true
           description: Numeric transaction ID"""

        # Set Env
        api_url = "%s/%s/transactions%s/%s" % (
            self.base_url,
            account_id_key,
            ".json" if resp_format == "json" else "",
            transaction_id,
        )

        # Build Payload
        payload = kwargs
        LOGGER.debug("payload: %s", payload)

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()
