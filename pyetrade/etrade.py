#!/usr/bin/env python3
'''etrade.py
   Description: Python interface to the eTrade API
   NOTES:
   Oauth package: rauth (considering) - rauth package will not work
                                        lacking ability to add other
                                        attributes
                  hashlib - generate HMAC-SHA1
   # Sandbox
   etrade = OAuth1Service(name='etrade',
                          #oauth_consumer_key='e51a0c96ee21b82c43f320e604ea5f5e',
                          consumer_key='e51a0c96ee21b82c43f320e604ea5f5e',
                          #oauth_timestamp=time.time(),
                          #oauth_nonce=nonce(9),
                          #oauth_signature_method='HMAC-SHA1',
                          consumer_secret='89a4aac688ea391c9bd7facfa40c1453',
                          request_token_url='https://etws.etrade.com/oauth/request_token',
                          access_token_url='https://etws.etrade.com/oauth/access_token',
                          authorize_url='https://us.etrade.com/e/t/etws/authorize',
                          base_url='https://etwssandbox.etrade.com/',
                          oauth_callback='oob')
   # Prod
   etrade = OAuth1Service(name='etrade',
                          consumer_key='e51a0c96ee21b82c43f320e604ea5f5e',
                          consumer_secret='89a4aac688ea391c9bd7facfa40c1453',
                          request_token_url='https://etws.etrade.com/oauth/request_token',
                          access_token_url='https://etws.etrade.com/oauth/access_token',
                          authorize_url='https://us.etrade.com/e/t/etws/authorize',
                          base_url='https://etws.etrade.com/accounts/rest/')

   # header
   header = {'Authorization': r'OAuth realm="",
                                oauth_callback="oob",
                                oauth_signature="",
                                oauth_nonce="LTg2ODUzOTQ5MTEzMTY3MzQwMzE%3D",
                                oauth_signature_method="HMAC-SHA1",
                                oauth_consumer_key="e51a0c96ee21b82c43f320e604ea5f5e",
                                oauth_timestamp="1273254425"'}
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
    * Authentication
    * Fix note formatting'''

from os import urandom
from base64 import b64encode

class ETradeAPI(object):
    '''ETradeAPI
       Main API class'''
    def __init__(self, dev=True):
        if dev:
            # eTrade sandbox url
            self.base_url = 'https://etwssandbox.etrade.com'
        else:
            # eTrade prod url
            self.base_url = 'https://etws.etrade.com'
