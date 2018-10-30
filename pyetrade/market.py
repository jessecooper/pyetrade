#!/usr/bin/python3

'''Market - ETrade Market API V1

    Requests that require detailed input, such as an order to buy or sell stock,
    use an HTTP POST request, with the parameters included as either XML or JSON data
    
    Generally, three different types of response that one can get from the routines based on the requested resp_format
        * None - return a python object
        * XML - return XML text straight from the Etrade API
        * JSON - return JSON text straight from the Etrade API

   TODO:
    * Look Up Product
    * Get Quote - Doc String'''

''' Calling sequence to get all option chains for a particular month
    me = pyetrade.market.ETradeMarket(
                    consumer_key,
                    consumer_secret, 
                    tokens['oauth_token'],
                    tokens['oauth_token_secret'],
                    dev = False)
    
    option_dates = me.get_option_expire_date('aapl', None)
    option_data = me.get_option_chain_data('aapl',strikes)
    
    or, all in one get all strikes for all future dates:
    (option_data,count) = me.get_all_option_data('aapl')

'''

import datetime as dt
from requests_oauthlib import OAuth1Session
import logging
from logging.handlers import RotatingFileHandler

# logger settings
LOGGER = logging.getLogger('my_logger')
LOGGER.setLevel(logging.DEBUG)
handler = RotatingFileHandler("etrade.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
LOGGER.addHandler(handler)


class ETradeMarket(object):
    '''ETradeMarket'''
    def __init__(self, client_key, client_secret, resource_owner_key, resource_owner_secret, dev=True):
        '''__init__(client_key, client_secret, resource_owner_key, resource_owner_secret, dev=True)
        
            This is the object initialization routine, which simply sets the various variables to be
            used by the rest of the methods and constructs the OAuth1Session.
            
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
            description: OAuth authentication token secret
           
            param: dev
            type: boolean
            description: use the sandbox environment (True) or live (False)
            
        '''
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.dev_environment = dev
        suffix = ('apisb' if dev else 'api')
        self.base_url = r'https://%s.etrade.com/v1/market/' % suffix
        self.session = OAuth1Session(self.client_key,
                                     self.client_secret,
                                     self.resource_owner_key,
                                     self.resource_owner_secret,
                                     signature_type='AUTH_HEADER')
        
    def __str__(self):
        ret = [ 'Use development environment: %s' % self.dev_environment,
                'base URL: %s' % self.base_url
                ]
        return '\n'.join(ret)

    def look_up_product(self, search_str, resp_format=None):
        '''look_up_product(company, s_type, resp_format='json')
        
           param: search_str
           type: str
           description: full or partial name of the company. Note
           that the system extensivly abbreviates common words
           such as company, industry and systems and generally
           skips punctuation
           
           param: resp_format
           type: str or None
           description: Response format json, xml, or None (python object)
           
           
           '''
           
        assert resp_format in ('json','xml',None)
        api_url = self.base_url + 'lookup/%s' % search_str
        if resp_format in ('json',None): api_url += '.json'
        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format is None:
            return req.json()
        else:
            return req.text

    def get_quote(self, args, resp_format=None, detail_flag='ALL'):
        ''' get_quote(resp_format, detail_flag, **kwargs)
        
            Get quote data on all symbols provided in the list args.
            the eTrade API is limited to 25 requests per call. Issue
            warning if more than 25 are requested. Only process the first 25.
        
            param: resp_format
            type: str
            description: Response format JSON text, XML test, or None for python object
           
            param: detailFlag
            type: enum
            required: optional
            description: Optional parameter specifying which details to
                return in the response. The field set for each possible
                value is listed in separate tables below. The possible
                values are:
                    * FUNDAMENTAL - Instrument fundamentals and latest
                        price
                    * INTRADAY - Performance for the current of most
                        recent trading day
                    * OPTIONS - Information on a given option offering
                    * WEEK_52 - 52-week high and low (highest high and
                        lowest low
                    * ALL (default) - All of the above information and
                        more
            kwargs:
            param: symbol
            type: list
            required: true
            description: One or more symobols
                for equities or options, up to a maximum of 25 symbols
                for equities are simple, e.g. GOOG. Symbols for options
                are more complex, consisting of six elements separated
                by colons, in this format:
                underlier:year:month:day:optionType:strikePrice
                
             param: adjNonAdjFlag
             type: bool
             description: Indicates whether an option has been adjusted
                due to a corporate action (e.g. a dividend or stock
                split). Possible values are TRUE, FALSE
                
             param: annualDividend
             type: double
             description: Cash amount paid per share over the past year
             
             param: ask
             type: double
             description: The current ask price for a security
             type: askExchange
                
                y=self.get_quote(['googl','aapl'])
                y['quoteResponse']['quoteData'][0]['all'] ==> dictionary for 1st element in return list
                
                y=self.get_quote(['AAPL:2018:05:18:put:150'])
                
            '''
            
        assert resp_format in ('json','xml', None)
        assert isinstance(args,list)
        if len(args) > 25: LOGGER.warning('get_quote asked for %d requests; only first 25 returned' % len(args))
        
        args_str = ','.join(args[:25])       # ensure that a max of 25 symbols are sent
        api_url = '%s/quote/%s' % (self.base_url, args_str)
        if resp_format in ('json',None): api_url += '.json'
        
        LOGGER.debug(api_url)
        payload = {'detailFlag': detail_flag}
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format is None:
            return req.json()
        else:
            return req.text

    def get_option_chains(self, underlier, expiry_date=None, skipAdjusted=None, chainType=None, resp_format=None,
                          strikePriceNear=None, noOfStrikes=None, optionCategory=None, priceType=None):
        ''' get_optionchains(underlier, expiry_date, skipAdjusted=True, chainType='callput', resp_format=None)
        
            Returns the option chain information for the requested expiry_date and chaintype in the desired format.
        
           param: underlier
           type: str
           description: market symbol
           
           param: chainType
           type: str
           description: put, call, or callput
           
           param: expiry_date
           type: dt.date()
           description: contract expiration date
           
           param: skipAdjusted
           type: bool
           description: Specifies whether to show (TRUE) or not show (FALSE) adjusted options, i.e., options 
                        that have undergone a change resulting in a modification of the option contract.
           
           param: resp_format
           type: str
           description: Response format json, xml, or None (python object)
           
           Sample Request
           GET https://api.etrade.com/v1/market/optionchains?expirationDay=03&expirationMonth=04&expirationYear=2011&chainType=PUT&skipAdjusted=true&symbol=GOOGL

        '''
#        assert expiry_date.year >= 2010
        assert resp_format in ('json', 'xml', None)
        assert chainType in ('put', 'call', 'callput', None)
        assert optionCategory in ('standard', 'all', 'mini', None)
        assert priceType in ('atmn', 'all', None)
        assert skipAdjusted in (True, False, None)
        
        args = ['symbol=%s' % underlier ]
        if expiry_date is not None:
            args.append('expirationDay=%02d&expirationMonth=%02d&expirationYear=%04d' % (expiry_date.day,expiry_date.month, expiry_date.year))
        if strikePriceNear is not None:
            args.append('strikePriceNear=%0.2f' % strikePriceNear)
        if chainType is not None:
            args.append('chainType=%s' % chainType)
        if optionCategory is not None:
            args.append('optionCategory=%s' % optionCategory.upper())
        if priceType is not None:
            args.append('priceType=%s' % priceType.upper())
        if skipAdjusted is not None:
            args.append('skipAdjusted=%s' % str(skipAdjusted))
        if noOfStrikes is not None:
            args.append('noOfStrikes=%d' % noOfStrikes.upper())
        api_url = self.base_url + 'optionchains?' + '&'.join(args)
        
        if resp_format in (None,'json'):
            req = self.session.get(api_url + '.json')
        else:
            req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(api_url)
        LOGGER.debug(req.text)

        if resp_format is None:
            return req.json()['OptionChainResponse']['OptionPair']
        else:
            return req.text

    def get_option_expire_date(self, underlier, resp_format=None):
        ''' get_option_expiry_dates(underlier, resp_format, **kwargs)
        
            If resp_format is None, return a list of datetime.date objects for the underlier, as returned by the Etrade API.
            Otherwise, return the XML or JSON text as appropriate for resp_format.
            
            param: underlier
            type: str
            description: market symbol
           
            param: resp_format
            type: str or None
            description: Response format json, xml, or None (python object)
           
            https://api.etrade.com/v1/market/optionexpiredate?symbol={symbol}
                
            Sample Request
            GET https://api.etrade.com/v1/market/optionexpiredate?symbol=GOOG&expiryType=ALL
            or  https://api.etrade.com/v1/market/optionexpiredate?symbol=GOOG&expiryType=ALL.json
            
        '''

        assert resp_format in (None,'json','xml')
        api_url = self.base_url + 'optionexpiredate?symbol=%s&expiryType=ALL' % underlier
        if resp_format in ('json',None): api_url += '.json'
        LOGGER.debug(api_url)
        
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format is None:
            z = req.json()['OptionExpireDateResponse']
            return [ dt.date(int(x['ExpirationDate']['year']), int(x['ExpirationDate']['month']), int(x['ExpirationDate']['day'])) for x in z ]
        else:
            return req.text
