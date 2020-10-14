"""Accounts - ETrade Accounts API Calls

   TODO:
       * Fix init doc string
       * Check request response for error

       """

import logging
import xmltodict
from requests_oauthlib import OAuth1Session

# Set up logging
LOGGER = logging.getLogger(__name__)


class ETradeAccounts(object):
    """:description: Accounts object to access account information

       :param client_key: Client key provided by Etrade
       :type client_key: str, required
       :param client_secret: Client secret provided by Etrade
       :type client_secret: str, required
       :param resource_owner_key: Resource key from :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_key: str, required
       :param resource_owner_secret: Resource secret from
            :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_secret: str, required
       :param dev: Defines Sandbox (True) or Live (False) ETrade, defaults to True
       :type dev: bool, optional
       :EtradeRef: https://apisb.etrade.com/docs/api/account/api-account-v1.html

        """

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
        """:description: Lists accounts in Etrade

           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: List of accounts
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/account/api-account-v1.html
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
        """:description: Retrieves account balanace for an account

           :param account_id_key: AccountIDkey retrived from :class:`list_accounts`
           :type  account_id_key: str, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: Balance of account with key ``account_id_key``
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/account/api-balance-v1.html
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
        """:description: Retrieves account portfolio for an account

           :param account_id_key: AccountIDkey retrived from :class:`list_accounts`
           :type  account_id_key: str, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :param kwargs: Parameters for api
           :type  kwargs: ``**kwargs``, optional
           :return: Account portfolio of account with key ``account_id_key``
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/account/api-portfolio-v1.html

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
        """:description: Retrieves transactions for an account

           :param account_id_key: AccountIDKey retrived from :class:`list_accounts`
           :type  account_id_key: str, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :param kwargs: Parameters for api
           :type  kwargs: ``**kwargs``, optional
           :return: Transactions list for account with key ``account_id_key``
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/account/api-transaction-v1.html
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
        """:description: Retrieves transaction details for an account

           :param account_id_key: AccountIDKey retrived from :class:`list_accounts`
           :type  account_id_key: str, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :param transaction_id: Numeric transaction ID obtained from :class:`list_transactions`
           :type  transaction_id: int, required
           :param kwargs: Parameters for api
           :type  kwargs: ``**kwargs``, optional
           :return: Transaction Details for ``transaction_id`` for account key ``account_id_key``
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/account/api-transaction-v1.html

           """

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
