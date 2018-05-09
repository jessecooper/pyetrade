#!/usr/bin/python3

'''Market - ETrade Market API
   TODO:
    * Look Up Product
    * Get Quote - Doc String'''

import logging
import datetime as dt
from requests_oauthlib import OAuth1Session
from pyetrade.etrade_exception import MarketQuoteException

# Set up logging
LOGGER = logging.getLogger(__name__)

# know when today is
TODAY = dt.date.today()
(THIS_YEAR, THIS_MONTH, THIS_DAY) = (TODAY.year, TODAY.month, TODAY.day)

class ETradeMarket(object):
    '''ETradeMarket'''
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
        self.base_url_prod = r'https://etws.etrade.com'
        self.base_url_dev = r'https://etwssandbox.etrade.com'
        self.session = OAuth1Session(self.client_key,
                                     self.client_secret,
                                     self.resource_owner_key,
                                     self.resource_owner_secret,
                                     signature_type='AUTH_HEADER')

    def look_up_product(self, company, s_type,
                        dev=True, resp_format='json'):
        '''look_up_product() -> resp
           param: company
           type: string
           description: full or partial name of the company. Note
           that the system extensivly abbreviates common words
           such as company, industry and systems and generally
           skips punctuation
           param: s_type
           type: enum
           description: the type of security. possible values are:
               * EQ (equity)
               * MF (mutual fund)
           rparam: companyName
           rtype: string
           rdescription: the company name
           rparam: exhange
           rtype: string
           rdescription: the exchange that lists that company
           rparam: securityType
           rtype: string
           rdescription: the type of security. EQ or MF
           rparam: symbol
           rtype: string
           rdescription: the market symbol for the security'''
        # Set Env join symbles with .join(args)
        if dev:
            if resp_format == 'json':
                uri = r'market/sandbox/rest/productlookup'
                api_url = '%s/%s.%s' % (
                    self.base_url_dev, uri, resp_format
                    )
            elif resp_format == 'xml':
                uri = r'market/sandbox/rest/productlookup'
                api_url = '%s/%s' % (self.base_url_dev, uri)
        else:
            if resp_format == 'json':
                uri = r'market/rest/productlookup'
                api_url = '%s/%s.%s' % (
                    self.base_url_prod, uri, resp_format
                    )
            elif resp_format == 'xml':
                uri = r'market/rest/productlookup'
                api_url = '%s/%s' % (self.base_url_prod, uri)
        LOGGER.debug(api_url)
        #add detail flag to url
        payload = {
            'company': company,
            'type': s_type
            }
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json()
        else:
            return req.text

    def get_quote(self, *args, dev=True, resp_format='json', detail_flag='ALL'):
        '''get_quote(dev, resp_format, **kwargs) -> resp
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format JSON or None = XML
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
                    * WEEK52 - 52-week high and low (highest high and
                        lowest low
                    * ALL (default) - All of the above information and
                        more
           args:
           param: symbol
           type: array
           required: true
           description: One or more (comma-seperated) symobols
                for equities or options, up to a maximum of 25 Symbols
                for equities are simple, e.g. GOOG. Symbols for options
                are more complex, consisting of six elements separated
                by colons, in this format:
                underlier:year:month:day:optionType:strikePrice
                        rparam: adjNonAdjFlag
            rtype: bool
            rdescription: Indicates whether an option has been adjusted
                due to a corporate action (e.g. a dividend or stock
                split). Possible values are TRUE, FALSE
            rparam: annualDividend
            rtype: double
            rdescription: Cash amount paid per share over the past year
            rparam: ask
            rtype: double
            rdescription: The current ask price for a security
            rtype: askExchange
            ...'''
        # exception if args > 25
        if len(args) > 25:
            raise MarketQuoteException
        # Set Env join symbles with .join(args)
        if dev:
            uri = r'market/sandbox/rest/quote/'+','.join(args)
            api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
        else:
            uri = r'market/rest/quote/'+','.join(args)
            api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)
        LOGGER.debug(api_url)
        #add detail flag to url
        payload = {'detailFlag': detail_flag}
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json()
        else:
            return req.text

    def get_optionchains(self, chainType='CALLPUT', expirationMonth=THIS_MONTH, expirationYear=THIS_YEAR, underlier='GOOGL', skipAdjusted=True,
                         dev=True, resp_format='json'):
        '''get_optionchains(dev, resp_format, **kwargs) -> resp
            
           param: chainType
           type: str
           description: CALL, PUT, or CALLPUT (both)
           
           param: expirationMonth
           type: int
           description: contract expiration month; number between 1 (January) and 12 (December)
           
           param: expirationYear
           type: int
           description: contract expiration year; number between 2012 and future year
           
           param: underlier
           type: str
           description: market symbol
           
           param: skipAdjusted
           type: bool
           description: Specifies whether to show (TRUE) or not show (FALSE) adjusted options, i.e., options 
                        that have undergone a change resulting in a modification of the option contract.
               
           param: dev
           type: bool
           description: API enviornment
           
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           
           Sample Request
           GET https://etws.etrade.com/market/rest/optionchains?expirationMonth=04&expirationYear=2011&chainType=PUT&skipAdjusted=true&underlier=GOOG

        '''
        assert 0 < expirationMonth <= 12
        assert expirationYear >= 2010
        assert (resp_format in ('json', 'xml', None))
        assert (chainType in ('CALLPUT','CALL','PUT'))
        
        # separator ',' instead of '&' to follow previous code; need '?' after optionchains?
        args_str = 'expirationMonth=%02d,expirationYear=%04d,underlier=%s,chainType=%s,skipAdjusted=%s' % (expirationMonth, expirationYear, underlier, chainType, str(skipAdjusted))
        
        if dev:
            uri = r'market/sandbox/rest/optionchains/'
            api_url = '%s/%s?%s.%s' % (self.base_url_dev, uri, args_str, resp_format)
        else:
            uri = r'market/rest/optionchains/'
            api_url = '%s/%s?%s.%s' % (self.base_url_prod, uri, args_str, resp_format)
        LOGGER.debug(api_url)
        
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json(), api_url
        else:
            return req.text, api_url


    def get_optionexpiredate(self, underlier='GOOGL',
                             dev=True, resp_format='json'):
        '''get_option_expiry_dates(dev, resp_format, **kwargs) -> resp
            
           param: underlier
           type: str
           description: market symbol
           
           param: dev
           type: bool
           description: API enviornment
           
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           
           Sample Request
           GET https://etws.etrade.com/market/rest/optionexpiredate?underlier=GOOGL
           
               https://etws.etrade.com/market/rest/optionexpiredate?underlier=GOOGL.json
        '''
        
        # separator ',' instead of '&' to follow previous code; need '?' after optionchains?
        args_str = 'underlier=%s' % underlier
        if dev:
            uri = r'market/sandbox/rest/optionexpiredate'
            api_url = '%s/%s?%s.%s' % (self.base_url_dev, uri, args_str, resp_format)
        else:
            uri = r'market/rest/optionexpiredate'
            api_url = '%s/%s?%s.%s' % (self.base_url_prod, uri, args_str, resp_format)
        LOGGER.debug(api_url)
        
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json(), api_url
        else:
            return req.text, api_url
