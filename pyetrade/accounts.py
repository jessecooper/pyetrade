import logging

import xmltodict
from requests_oauthlib import OAuth1Session

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
        client_key: str,
        client_secret: str,
        resource_owner_key: str,
        resource_owner_secret: str,
        dev: bool = True,
    ):
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.base_url = f'https://{"apisb" if dev else "api"}.etrade.com/v1/accounts'
        self.session = OAuth1Session(
            self.client_key,
            self.client_secret,
            self.resource_owner_key,
            self.resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_accounts(self, resp_format: str = "xml") -> dict:
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
        self,
        account_id_key: str,
        account_type: str = None,
        real_time: bool = True,
        resp_format: str = "xml",
    ) -> dict:
        """:description: Retrieves account balance for an account

        :param account_id_key: AccountIDkey retrieved from :class:`list_accounts`
        :type  account_id_key: str, required
        :param account_type: The registered account type, defaults to None
        :type  account_type: str, optional
        :param real_time: Use real time balance or not, defaults to True
        :type  real_time: bool, optional
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
        self,
        account_id_key: str,
        count: int = 50,
        sort_by: str = None,
        sort_order: str = "DESC",
        page_number: int = None,
        market_session: str = "REGULAR",
        totals_required: bool = False,
        lots_required: bool = False,
        view: str = "QUICK",
        resp_format: str = "xml",
    ) -> dict:
        """:description: Retrieves account portfolio for an account

        :param account_id_key: AccountIDkey retrieved from :class:`list_accounts`
        :type  account_id_key: str, required
        :param count: The number of positions to return in the response, defaults to 50
        :type  count: int, optional
        :param sort_by: Sorting done based on the column specified in the query parameter.
        :type  sort_by: str, optional
        :param sort_order: Sort orders (ASC or DESC), defaults to DESC
        :type  sort_order: str, optional
        :param page_number: The specific page that in the list that is to be returned. Each page has a default count of 50 positions.  # noqa: E501
        :type  page_number: int, optional
        :param market_session: The market session (Regular or Extended), defaults to REGULAR
        :type  market_session: str, optional
        :param totals_required: It gives the total values of the portfolio, defaults to False
        :type  totals_required: bool, optional
        :param lots_required: It gives position lots for positions, defaults to False
        :type  lots_required: bool, optional
        :param view: The view query: PERFORMANCE, FUNDAMENTAL, OPTIONSWATCH, QUICK, COMPLETE. Defaults to QUICK.
        :type  view: str, optional
        :param resp_format: Desired Response format, defaults to xml
        :type  resp_format: str, optional
        :return: Account portfolio of account with key ``account_id_key``
        :rtype: xml or json based on ``resp_format``
        :EtradeRef: https://apisb.etrade.com/docs/api/account/api-portfolio-v1.html
        """

        api_url = "%s/%s/portfolio%s" % (
            self.base_url,
            account_id_key,
            ".json" if resp_format == "json" else "",
        )

        payload = {
            "count": count,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "pageNumber": page_number,
            "marketSession": market_session,
            "totalsRequired": totals_required,
            "lotsRequired": lots_required,
            "view": view,
        }

        LOGGER.debug(api_url)

        req = self.session.get(api_url, params=payload)
        req.raise_for_status()

        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def get_portfolio_position_lot(
        self, symbol: str, account_id_key: str, resp_format: str = "xml"
    ) -> dict:
        """:description: Retrieves account portfolio position lot based on provided symbol

        :param symbol: Desired equity symbol to search for position lots in desired account portfolio
        :type  symbol: str, required
        :param account_id_key: AccountIDkey retrieved from :class:`list_accounts`
        :type  account_id_key: str, required
        :param resp_format: Desired Response format, defaults to xml
        :type  resp_format: str, optional
        :return: PositionLot of ``symbol`` in account portfolio of account with key ``account_id_key``
        :rtype: xml or json based on ``resp_format``
        :EtradeRef: https://apisb.etrade.com/docs/api/account/api-portfolio-v1.html
        """

        account_portfolio = self.get_account_portfolio(
            account_id_key, lots_required=True, resp_format="json"
        )["PortfolioResponse"]["AccountPortfolio"][0]["Position"]

        lot_position_id = [
            position["positionId"]
            for position in account_portfolio
            if symbol.upper() == position["Product"]["symbol"].upper()
        ]

        # If the symbol exists then there should only be one ID filtered from the portfolio response
        if len(lot_position_id) != 1:
            raise KeyError(
                f'Symbol "{symbol}" could not be found in the current portfolio. '
                f"Please check your portfolio and symbol before trying again."
            )

        LOGGER.debug(lot_position_id[0])

        api_url = "%s/%s/portfolio/%s%s" % (
            self.base_url,
            account_id_key,
            lot_position_id[0],
            ".json" if resp_format == "json" else "",
        )

        req = self.session.get(api_url)
        req.raise_for_status()

        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def list_transactions(
        self,
        account_id_key: str,
        start_date: str = None,
        end_date: str = None,
        sort_order: str = "DESC",
        marker=None,
        count: int = 50,
        resp_format: str = "xml",
    ) -> dict:
        """:description: Retrieves transactions for an account

        :param account_id_key: AccountIDKey retrieved from :class:`list_accounts`
        :type  account_id_key: str, required
        :param start_date: The earliest date to include in the date range, formatted as MMDDYYYY (history is available for two years), default is None  # noqa: E501
        :type  start_date: str, optional
        :param end_date: The latest date to include in the date range, formatted as MMDDYYYY, default is None
        :type  end_date: `str, optional
        :param sort_order: The sort order request (ASC or DESC), default is DESC
        :type  sort_order: str, optional
        :param marker: Specifies the desired starting point of the set of items to return (used for paging), default is None  # noqa: E501
        :type  marker: ??, optional
        :param count: Number of transactions to return in the response, default is 50
        :type  count: int, optional
        :param resp_format: Desired Response format, defaults to xml
        :type  resp_format: str, optional
        :return: Transactions list for account with key ``account_id_key``
        :rtype: xml or json based on ``resp_format``
        :EtradeRef: https://apisb.etrade.com/docs/api/account/api-transaction-v1.html
        """

        api_url = "%s/%s/transactions%s" % (
            self.base_url,
            account_id_key,
            ".json" if resp_format == "json" else "",
        )

        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "sortOrder": sort_order,
            "marker": marker,
            "count": count,
        }

        LOGGER.debug(api_url)

        req = self.session.get(api_url, params=payload)
        req.raise_for_status()

        LOGGER.debug(req.text)

        # Depending on when transactions are completed and start/end date
        # restrictions, it's possible for the response to return nothing: ""
        if req.text == "":
            return {}
        elif resp_format.lower() == "xml":
            return xmltodict.parse(req.text)
        else:
            return req.json()

    def list_transaction_details(
        self,
        account_id_key: str,
        transaction_id: int,
        resp_format: str = "xml",
        **kwargs,
    ) -> dict:
        """:description: Retrieves transaction details for an account

        :param account_id_key: AccountIDKey retrieved from :class:`list_accounts`
        :type  account_id_key: str, required
        :param transaction_id: Numeric transaction ID obtained from :class:`list_transactions`
        :type  transaction_id: int, required
        :param resp_format: Desired Response format, defaults to xml
        :type  resp_format: str, optional
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

        LOGGER.debug(api_url)

        req = self.session.get(api_url, params=kwargs)
        req.raise_for_status()

        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()
