#!/usr/bin/env python3
'''etrade.py
   Description: Python interface to the eTrade API
   NOTES:
   Oauth 1.0a package: requests_oauthlib
   TODO:
    * renew_access_token
    * Fix doc strings
    * Lint this messy code'''

from requests_oauthlib import OAuth1Session

class ETradeAPI(object):
    '''ETradeAPI
       Main API class'''
    def __init__(self, consumer_key, consumer_secret, callback_url = 'oob'):
        '''__init__(consumer_key, consumer_secret, callback_url)
           param: consumer_key
           type: str
           description: etrade oauth consumer key
           param: consumer_secret
           type: str
           description: etrade oauth consumer secret
           param: callback_url
           type: str
           description: etrade oauth callback url default oob'''

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url_prod = r'https://etws.etrade.com'
        self.base_url_dev = r'https://etwssandbox.etrade.com'
        self.req_token_url = r'https://etws.etrade.com/oauth/request_token'
        self.auth_token_url = r'https://us.etrade.com/e/t/etws/authorize'
        self.access_token_url = r'https://etws.etrade.com/oauth/access_token'
        self.callback_url = callback_url
        self.access_token = None
        self.resource_owner_key = None

    def get_request_token(self):
        '''get_request_token() -> auth url
        rtype: str'''

        # Set up session
        self.session = OAuth1Session(self.consumer_key,
                                     self.consumer_secret,
                                     callback_uri = self.callback_url,
                                     signature_type = 'AUTH_HEADER')
        # get request token
        self.session.fetch_request_token(self.req_token_url)
        # get authorization url
        #etrade format: url?key&token
        authorization_url = self.session.authorization_url(self.auth_token_url)
        akey = self.session.parse_authorization_response(authorization_url)
        # store oauth_token
        self.resource_owner_key = akey['oauth_token']
        formated_auth_url = '%s?key=%s&token=%s' % (self.auth_token_url,
                                                    self.consumer_key,
                                                    akey['oauth_token'])
        self.verifier_url = formated_auth_url
        #print('Please go here and authorize, %s' %  formated_auth_url)
        return formated_auth_url


    def get_access_token(self, verifier):
        '''get_access_token(verifier, dev) -> void
           param: verifier
           type: str
           description: oauth verification code
           param: dev
           type: bool
           description: etrade dev or prod env
           notes:
           get redirect url
           redirect_url = redirect_response = raw_input('Paste the full redirect URL here: ')
           get varification code
           session.parse_authorization_response(redirect_url)
           get access token TODO move out into object function
           session.fetch_access_token('https://etws.etrade.com/oauth/access_token')'''

        # Set verifier
        self.session._client.client.verifier = verifier
        # Get access token
        self.access_token = self.session.fetch_access_token(self.access_token_url)

        return self.access_token

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

        
