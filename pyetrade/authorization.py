#!/usr/bin/env python3

'''authorization.py
   Description: ETrade API authorization
   TODO:
    * Lint this messy code
    * Catch events'''

import logging
from requests_oauthlib import OAuth1Session
# Set up logging
logger = logging.getLogger(__name__)

class ETradeOAuth(object):
    '''ETradeOAuth
       ETrade OAuth 1.0a Wrapper'''
    def __init__(self, consumer_key, consumer_secret, callback_url='oob'):
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
           some params handled by requests_oauthlib but put in
           doc string for clarity into the API.
           param: oauth_consumer_key
           type: str
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           description: the date and time of the request, in epoch time.
                        must be accurate within five minutes.
           param: oauth_nonce
           type: str
           description: a nonce, as discribed in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           description: the signature method used by the consumer to sign
                        the request. the only supported value is 'HMAC-SHA1'.
           param: oauth_signature
           type: str
           description: signature generated with the shared secret and token
                        secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_callback
           type: str
           description: callback information, as described elsewhere. must
                        always be set to 'oob' whether using a callback or
                        not
           rtype: str
           description: Etrade autherization url'''

        # Set up session
        self.session = OAuth1Session(self.consumer_key,
                                     self.consumer_secret,
                                     callback_uri=self.callback_url,
                                     signature_type='AUTH_HEADER')
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
           description: oauth access tokens

           OAuth API paramiters mostly handled by requests_oauthlib
           but illistrated here for clarity.
           param: oauth_consumer_key
           type: str
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           description: the date and time of the request, in epoch time.
                        must be accurate within five minutes.
           param: oauth_nonce
           type: str
           description: a nonce, as discribed in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           description: the signature method used by the consumer to sign
                        the request. the only supported value is 'HMAC-SHA1'.
           param: oauth_signature
           type: str
           description: signature generated with the shared secret and token
                        secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_token
           type: str
           description: the consumer's request token to be exchanged for an
                        access token
           param: oauth_verifier
           type: str
           description: the code received by the user to authenticate with
                        the third-party application'''

        # Set verifier
        self.session._client.client.verifier = verifier
        # Get access token
        self.access_token = self.session.fetch_access_token(self.access_token_url)
        logger.debug(self.access_token)

        return self.access_token

class ETradeAccessManager(object):
    '''ETradeAccessManager - Renew and revoke ETrade OAuth Access Tokens'''
    def __init__(self, client_key, client_secret,
                 resource_owner_key, resource_owner_secret):
        '''__init__(client_key, client_secret)
           param: client_key
           type: str
           description: etrade client key
           param: client_secret
           type: str
           description: etrade client secret
           param: resource_owner_key
           type: str
           description: OAuth authentication token key
           param: resource_owner_secret
           type: str
           description: OAuth authentication token secret'''
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.renew_access_token_url = r'https://etws.etrade.com/oauth/renew_access_token'
        self.revoke_access_token_url = r'https://etws.etrade.com/oauth/revoke_access_token'
        self.session = OAuth1Session(self.client_key,
                                     self.client_secret,
                                     self.resource_owner_key,
                                     self.resource_owner_secret,
                                     signature_type='AUTH_HEADER')

    def renew_access_token(self):
        '''renew_access_token() -> bool
           some params handled by requests_oauthlib but put in
           doc string for clarity into the API.
           param: oauth_consumer_key
           type: string
           required: true
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           required: true
           description: the date and time of the request, in epoch time.
                        must be accurate withiin five minutes.
           param: oauth_nonce
           type: str
           required: true
           description: a nonce, as described in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           required: true
           description: the signature method used by the consumer to sign
                        the request. the only supported value is "HMAC-SHA1".
           param: oauth_signature
           type: str
           required: true
           description: signature generated with the shared secret and
                        token secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_token
           type: str
           required: true
           description: the consumer's access token to be renewed.'''
        resp = self.session.get(self.renew_access_token_url) 
        logger.debug(resp.text)
        resp.raise_for_status()

        return True

    def revoke_access_token(self):
        '''revoke_access_token() -> bool
           some params handled by requests_oauthlib but put in
           doc string for clarity into the API.
           param: oauth_consumer_key
           type: string
           required: true
           description: the value used by the consumer to identify
                        itself to the service provider.
           param: oauth_timestamp
           type: int
           required: true
           description: the date and time of the request, in epoch time.
                        must be accurate withiin five minutes.
           param: oauth_nonce
           type: str
           required: true
           description: a nonce, as described in the authorization guide
                        roughly, an arbitrary or random value that cannot
                        be used again with the same timestamp.
           param: oauth_signature_method
           type: str
           required: true
           description: the signature method used by the consumer to sign
                        the request. the only supported value is "HMAC-SHA1".
           param: oauth_signature
           type: str
           required: true
           description: signature generated with the shared secret and
                        token secret using the specified oauth_signature_method
                        as described in OAuth documentation.
           param: oauth_token
           type: str
           required: true
           description: the consumer's access token to be revoked.'''
        resp = self.session.get(self.revoke_access_token_url)
        logger.debug(resp.text)
        resp.raise_for_status()

        return True
