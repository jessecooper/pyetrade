#!/usr/bin/python3

'''Accounts - ETrade Accounts API
   Calls
   TODO:
       * Get Transaction History
       * Get Transaction Details
       * List Alerts
       * Read Alert
       * Delete Alert
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
        '''get_account_positions(dev, resp_format)
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
