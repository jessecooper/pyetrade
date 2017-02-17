#!/usr/bin/python3

'''Order - ETrade Order API
   TODO:
       * Fix init doc string
       * List Order
       * Preview Equity Order
       * Place equity order
       * Preview equity order change
       * Place equity order change
       * Preview option order
       * Place option order
       * Preview option order change
       * Place option order change
       * Cancel Order'''

import logging
from requests_oauthlib import OAuth1Session
# Set up logging
logger = logging.getLogger(__name__)

class ETradeOrder(object):
    '''ETradeOrder:'''
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
                                     signature_type = 'AUTH_HEADER')

    def place_equity_order(self, dev = True, resp_format = 'json'):
        '''place_equity_order(dev, resp_format)
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
            uri = r'order/sandbox/rest/placeequityorder'
            api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
        else:
            uri = r'order/rest/placeequityorder'
            api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)

        logger.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text()

