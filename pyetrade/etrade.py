#!/usr/bin/env python3
'''etrade.py
   Description: Python interface to the eTrade API
   TODO:
    * Authentication
    * Everything else'''

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
