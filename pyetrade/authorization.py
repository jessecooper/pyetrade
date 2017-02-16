#!/usr/bin/env python3

'''authorization.py
   Description: ETrade API authorization
   TODO:
    * Fix doc strings
    * Lint this messy code
    * Add logging
    * Catch events
    * Revoke token'''

import logging
from requests_oauthlib import OAuth1Session
# Set up logging
logger = logging.getLogger(__name__)

class ETradeOAuth(object):
    '''ETradeOAuth
       ETrade OAuth 1.0a Wrapper'''
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
        self.renew_access_token_url = r'https://etws.etrade.com/oauth/renew_access_token'
        self.callback_url = callback_url
        self.access_token = None
        self.resource_owner_key = None

    def get_request_token(self):
        '''get_request_token() -> auth url
        rtype: str
        description: Etrade autherization url'''

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
        logger.debug(formated_auth_url)

        return formated_auth_url

    def get_access_token(self, verifier):
        '''get_access_token(verifier) -> access_token
           param: verifier
           type: str
           description: oauth verification code
           rtype: dict
           description: oauth access tokens'''

        # Set verifier
        self.session._client.client.verifier = verifier
        # Get access token
        self.access_token = self.session.fetch_access_token(self.access_token_url)

        return self.access_token

    def renew_access_token(self):
        '''renew_access_token() -> bool'''
        resp = self.session.get(self.renew_access_token_url)
        
        logger.debug(resp.text)
        resp.raise_for_status()
        
        return True
