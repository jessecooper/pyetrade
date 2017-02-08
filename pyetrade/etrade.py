#!/usr/bin/env python3
'''etrade.py
   Description: Python interface to the eTrade API
   NOTES:
   Oauth 1.0a package: requests_oauthlib
   # Request token
   URL
   https://etws.etrade.com/oauth/request_token
   HTTP Method: GET
   Request Parameters
   Property    Type    Description
   oauth_consumer_key  string  The value used by the consumer to identify itself to the service provider.
   oauth_timestamp integer The date and time of the request, in epoch time. Must be accurate within five minutes.
   oauth_nonce string  A nonce, as described in the authorization guide - roughly, an arbitrary or random value that cannot be used again with the same timestamp.
   oauth_signature_method  string  The signature method used by the consumer to sign the request. The only supported value is "HMAC-SHA1".
   oauth_signature string  Signature generated with the shared secret and token secret using the specified oauth_signature_method, as described in OAuth documentation.
   oauth_callback  string  Callback information, as described elsewhere. Must always be set to "oob", whether using a callback or not.

   # Access Token
   URL
   https://etws.etrade.com/oauth/access_token
   HTTP Method: GET
   Request Parameters:

   Property: oauth_consumer_key  
   Type: string
   Required: Required
   Description: The value used by the consumer to identify itself to the service provider.
   
   oauth_timestamp integer Required    The date and time of the request, in epoch time. Must be accurate to within five minutes.
   oauth_nonce string  Required    A nonce, as described in the authorization guide - roughly, an arbitrary or random value that cannot be used again with the same timestamp.
   oauth_signature_method  string  Required    The signature method used by the consumer to sign the request. The only supported value is "HMAC-SHA1".
   oauth_signature string  Required    Signature generated with the shared secret and token secret using the specified oauth_signature_method, as described in OAuth documentation.
   oauth_token string  Required    The consumer’s request token to be exchanged for an access token.
   oauth_verifier  string  Required    The code received by the user to authenticate with the third-party application.
   # Authorization
   URL
   https://us.etrade.com/e/t/etws/authorize?key={oauth_consumer_key}&token={oauth_token}
   HTTP Method: GET
   Request Parameters
   Property  Type    Required?   Description
   oauth_consumer_key  string  Required    The value used by the consumer to identify itself to the service provider.
   oauth_token   string  Required    The consumer’s request token.
   TODO:
    * renew_access_token
    * Fix note formatting'''

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
        self.req_token_url = 'https://etws.etrade.com/oauth/request_token'
        self.auth_token_url = 'https://us.etrade.com/e/t/etws/authorize'
        self.access_token_url = 'https://etws.etrade.com/oauth/access_token'
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
        formated_auth_url = '%s?key=%s&token=%s' % (self.auth_token_url, self.consumer_key, akey['oauth_token'])
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
        print(self.access_token)
