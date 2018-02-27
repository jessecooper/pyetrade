#!/usr/bin/python3

'''Accounts - ETrade Accounts API
   Calls
   TODO:
       * Fix init doc string
       * Check request response for error'''

import logging
from requests_oauthlib import OAuth1Session
# Set up logging
logger = logging.getLogger(__name__)

class ETradeAccounts(object):
    '''ETradeAccounts:'''
    def __init__(self, client_key, client_secret,
                 resource_owner_key, resource_owner_secret):
        '''__init_()
           '''
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.base_url_prod = r'https://etws.etrade.com'
        self.base_url_dev = r'https://etwssandbox.etrade.com'
        self.session = OAuth1Session(self.client_key,
                                     self.client_secret,
                                     self.resource_owner_key,
                                     self.resource_owner_secret,
                                     signature_type='AUTH_HEADER')

    def list_accounts(self, dev=True, resp_format='json'):
        '''list_account(dev, resp_format)
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        if dev:
            uri = r'accounts/sandbox/rest/accountlist'
            api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
        else:
            uri = r'accounts/rest/accountlist'
            api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)

        logger.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def get_account_balance(self, account_id, dev=True, resp_format='json'):
        '''get_account_balance(dev, resp_format)
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
           rtype: str'''

        if dev:
            uri = r'accounts/sandbox/rest/accountbalance'
            api_url = '%s/%s/%s.%s' % (
                    self.base_url_dev,
                    uri,
                    account_id,
                    resp_format
                )
        else:
            uri = r'accounts/rest/accountbalance'
            api_url = '%s/%s/%s.%s' % (
                    self.base_url_prod,
                    uri,
                    account_id,
                    resp_format
                )

        logger.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def get_account_positions(self, account_id, dev=True, resp_format='json'):
        '''get_account_positions(dev, account_id, resp_format) -> resp
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
           rtype: str'''

        if dev:
            uri = r'accounts/sandbox/rest/accountpositions'
            if resp_format is 'json':
                api_url = '%s/%s/%s.%s' % (
                        self.base_url_dev,
                        uri,
                        account_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s/%s' % (
                        self.base_url_dev,
                        uri,
                        account_id
                    )

        else:
            uri = r'accounts/rest/accountpositions'
            if resp_format is 'json':
                api_url = '%s/%s/%s.%s' % (
                        self.base_url_prod,
                        uri,
                        account_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                    api_url = '%s/%s/%s' % (
                        self.base_url_prod,
                        uri,
                        account_id
                    )

        logger.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def list_alerts(self, dev=True, resp_format='json'):
        '''list_alerts(dev, resp_format) -> resp
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str'''

        if dev:
            uri = r'accounts/sandbox/rest/alerts'
            if resp_format is 'json':
                api_url = '%s/%s.%s' % (
                        self.base_url_dev,
                        uri,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s' % (
                        self.base_url_dev,
                        uri,
                    )

        else:
            uri = r'accounts/rest/alerts'
            if resp_format is 'json':
                api_url = '%s/%s.%s' % (
                        self.base_url_prod,
                        uri,
                        resp_format
                    )
            elif resp_format is 'xml':
                    api_url = '%s/%s' % (
                        self.base_url_prod,
                        uri,
                    )

        logger.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def read_alert(self, alert_id, dev=True, resp_format='json'):
        '''read_alert(alert_id, dev, resp_format) -> resp
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
           rtype: str'''

        if dev:
            uri = r'accounts/sandbox/rest/alerts'
            if resp_format is 'json':
                api_url = '%s/%s/%s.%s' % (
                        self.base_url_dev,
                        uri,
                        alert_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s/%s' % (
                        self.base_url_dev,
                        uri,
                        alert_id
                    )

        else:
            uri = r'accounts/rest/alerts'
            if resp_format is 'json':
                api_url = '%s/%s/%s.%s' % (
                        self.base_url_prod,
                        uri,
                        alert_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                    api_url = '%s/%s/%s' % (
                        self.base_url_prod,
                        uri,
                        alert_id
                    )

        logger.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def delete_alert(self, alert_id, dev=True, resp_format='json'):
        '''delete_alert(alert_id, dev, resp_format) -> resp
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
           rtype: str'''

        if dev:
            uri = r'accounts/sandbox/rest/alerts'
            if resp_format is 'json':
                api_url = '%s/%s/%s.%s' % (
                        self.base_url_dev,
                        uri,
                        alert_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s/%s' % (
                        self.base_url_dev,
                        uri,
                        alert_id
                    )

        else:
            uri = r'accounts/rest/alerts'
            if resp_format is 'json':
                api_url = '%s/%s/%s.%s' % (
                        self.base_url_prod,
                        uri,
                        alert_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                    api_url = '%s/%s/%s' % (
                        self.base_url_prod,
                        uri,
                        alert_id
                    )

        logger.debug(api_url)
        req = self.session.delete(api_url)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def get_transaction_history(self, account_id, dev=True,
                    group = 'ALL',
                    asset_type = 'ALL',
                    transaction_type = 'ALL',
                    ticker_symbol = 'ALL',
                    resp_format='json', **kwargs):
        '''get_transaction_history(account_id, dev, resp_format) -> resp

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
           description: see ETrade API docs'''

        # add each optional argument not equal to 'ALL' to the uri
        optional_args = [group, asset_type, transaction_type, ticker_symbol]
        optional_uri = ''
        for optional_arg in optional_args:
            if optional_arg.upper() != 'ALL':
                optional_uri = '%s/%s' % (
                    optional_uri,
                    optional_arg
                )
        # Set Env
        if dev:
            #assemble the following:
            #self.base_url_dev: https://etws.etrade.com
            #uri:               /accounts/rest
            #account_id:        /{accountId}
            #format string:     /transactions
            # if not 'ALL' args:
            #   group:              /{Group}
            #   asset_type          /{AssetType}
            #   transaction_type:   /{TransactionType}
            #   ticker_symbol:      /{TickerSymbol}
            #resp_format:       {.json}
            #payload:           kwargs
            #
            uri = r'accounts/sandbox/rest'
            if resp_format is 'json':
                api_url = '%s/%s/%s/transactions%s.%s' % (
                        self.base_url_dev,
                        uri,
                        account_id,
                        optional_uri,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s/%s/transactions%s' % (
                        self.base_url_dev,
                        uri,
                        account_id,
                        optional_uri
                    )
        else:
            uri = r'accounts/rest'
            if resp_format is 'json':
                api_url = '%s/%s/%s/transactions%s.%s' % (
                        self.base_url_prod,
                        uri,
                        account_id,
                        optional_uri,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s/%s/transactions%s' % (
                        self.base_url_prod,
                        uri,
                        account_id,
                        optional_uri
                    )

        # Build Payload
        payload = kwargs
        logger.debug('payload: %s', payload)

        logger.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def get_transaction_details(self, account_id, transaction_id, dev=True,
                    resp_format='json', **kwargs):
        '''get_transaction_details(account_id, transaction_id, dev, resp_format) -> resp

           param: account_id
           type: int
           required: true
           description: Numeric account ID

           param: transaction_id
           type: int
           required: true
           description: Numeric transaction ID'''

        # Set Env
        if dev:
            uri = r'accounts/sandbox/rest'
            if resp_format is 'json':
                api_url = '%s/%s/%s/transactions/%s.%s' % (
                        self.base_url_dev,
                        uri,
                        account_id,
                        transaction_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s/%s/transactions/%s' % (
                        self.base_url_dev,
                        uri,
                        account_id,
                        transaction_id
                    )
        else:
            uri = r'accounts/rest'
            if resp_format is 'json':
                api_url = '%s/%s/%s/transactions/%s.%s' % (
                        self.base_url_prod,
                        uri,
                        account_id,
                        transaction_id,
                        resp_format
                    )
            elif resp_format is 'xml':
                api_url = '%s/%s/%s/transactions/%s' % (
                        self.base_url_prod,
                        uri,
                        account_id,
                        transaction_id
                    )

        # Build Payload
        payload = kwargs
        logger.debug('payload: %s', payload)

        logger.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text
