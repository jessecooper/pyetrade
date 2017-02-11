#!/usr/bin/python3
'''Accounts - ETrade Accounts API
   Calls'''

from requests_oauthlib import OAuth1Session

class ETradeAccounts(object):
    '''ETradeAccounts:'''
    def __init__(self, client_key, client_secret,
                 resource_owner_key, resource_owner_secret):
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
                                     signature_type = 'AUTH_HEADER')

    def list_account(self, dev = True, resp_format = 'json'):
        '''list_account(bool) -> obj'''

        # TODO: change resp_format to support default xml
        #       returns as well
        # 'https://etws.etrade.com/accounts/rest/accountlist'
        if dev:
            uri = r'accounts/sandbox/rest/accountlist'
        else:
            uri = r'accounts/rest/accountlist'

        api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
        print(api_url)
        req = self.session.get(api_url)

        return req

