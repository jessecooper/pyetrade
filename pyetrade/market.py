#!/usr/bin/python3

'''Market - ETrade Market API V1

    Generally, three different types of response that one can get from these routines are based on the requested resp_format
        * None - return a python object
        * XML - return XML text straight from the Etrade API

    Calling sequence to get all option chains for a particular month
    me = pyetrade.market.ETradeMarket(
                    consumer_key,
                    consumer_secret, 
                    tokens['oauth_token'],
                    tokens['oauth_token_secret'],
                    dev = False)
    
    option_dates = me.get_option_expire_date('aapl', None)
    option_chains = me.get_option_chains('aapl', None)
    
    OR all inclusive:
        (option_dates,option_chains) = me.get_all_option_chains('aapl')
    
'''

import datetime as dt
from requests_oauthlib import OAuth1Session
import xml.etree.ElementTree as ET
import logging
LOGGER = logging.getLogger(__name__)


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
        '''look_up_product(company, search_str, resp_format=None)
        
           param: search_str
           type: str
           description: full or partial name of the company. Note
           that the system extensivly abbreviates common words
           such as company, industry and systems and generally
           skips punctuation.
           
           param: resp_format
           type: 'xml' or None
           description: Response format xml or None (python object)
           
           '''
           
        assert resp_format in ('xml',None)
        api_url = self.base_url + 'lookup/%s' % search_str
        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)
        
        if resp_format=='xml':
            return req.text
        else:
            try:
                root = ET.fromstring(req.text)
            except:
                raise
            
            rtn = list()
            for a in root.findall('Data'):
                rtn.append({i.tag:i.text for i in a.getchildren() })
            return rtn

    def get_quote(self, symbols, resp_format=None, detail_flag=None, requireEarningsDate=None, skipMiniOptionsCheck=None):
        ''' get_quote(symbols, resp_format=None, detail_flag=None, requireEarningsDate=None, skipMiniOptionsCheck=None)
        
            Get quote data on all symbols provided in the list args.
            the eTrade API is limited to 25 requests per call. Issue
            warning if more than 25 are requested. Only process the first 25.
        
            param: resp_format
            type: 'json', 'xml' or None
            description: Response format JSON text, XML test, or None for python object
        
            param: skipMiniOptionsCheck
            type: True, False, None
            description: If value is true, no call is made to the service to check whether the symbol has mini options.
            If value is false or if the field is not specified, a service call is made to check if the symbol has mini options
           
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
                    * MF_DETAIL - MutualFund structure gets displayed.
                        
            param: symbols
            type: list
            required: true
            description: One or more symobols for equities or options, up to a maximum of 25 symbols.
                For equities, the symbol name alone, e.g. GOOGL.
                Symbols for options are more complex, consisting of six elements separated
                by colons, in this format:
                underlier:year:month:day:optionType:strikePrice
            '''
            
        assert resp_format in ('xml', None)
        assert detail_flag in ('fundamental','intraday','options','week_52','all','mf_detail', None)
        assert requireEarningsDate in (True, False, None)
        assert skipMiniOptionsCheck in (True, False, None)
        assert isinstance(symbols,list)
        if len(symbols) > 25: LOGGER.warning('get_quote asked for %d requests; only first 25 returned' % len(symbols))
        
        args = list()
        if detail_flag is not None:
            args.append('detail_flag=%s'%detail_flag.upper())
        if requireEarningsDate is not None:
            args.append('requireEarningsDate=%s'%str(requireEarningsDate))
        if skipMiniOptionsCheck is not None:
            args.append('skipMiniOptionsCheck=%s'%str(skipMiniOptionsCheck))
        
        api_url = self.base_url + 'quote/' + ','.join(symbols[:25])
        if len(args):
            api_url += '&' + '&'.join(args)
        LOGGER.debug(api_url)
        
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format=='xml':
            return req.text
        else:
            try:
                root = ET.fromstring(req.text)
            except:
                raise
            
            rtn = list()
            for a in root.findall('QuoteData'):
                this_rtn = { j.tag: j.text for j in a.find('Product') }
                this_rtn['dateTimeUTC'] = int(a.find('dateTimeUTC').text)
                for j in a.find('All').getchildren():
                    try:
                        this_rtn[j.tag] = float(j.text)
                    except:
                        this_rtn[j.tag] = j.text
                rtn.append(this_rtn)
            return rtn

    def get_all_option_chains(self, underlier):
        ''' Returns the expiration_dates and all the option chains for the underlier. This requires two calls, one to get_option_expire_date
            to get all the expiration_dates and multiple calls to get_option_chains with defaults.
        
            param: underlier
            type: str
            description: market symbol
            
        '''
        try:
            expiration_dates = self.get_option_expire_date(underlier,resp_format=None)
        except:
            raise
        rtn = list()
        for this_expiry_date in expiration_dates:
           rtn += self.get_option_chains(underlier, this_expiry_date, resp_format=None)
        return (expiration_dates, rtn)

    def get_option_chains(self, underlier, expiry_date=None, skipAdjusted=None, chainType=None, resp_format=None,
                          strikePriceNear=None, noOfStrikes=None, optionCategory=None, priceType=None):
        ''' get_optionchains(underlier, expiry_date=None, skipAdjusted=None, chainType=None, resp_format=None,
                             strikePriceNear=None, noOfStrikes=None, optionCategory=None, priceType=None)
        
            Returns the option chain information for the requested expiry_date and chaintype in the desired format.
            This should be a list of dictionaries, one for each option chain.
        
            param: underlier
            type: str
            description: market symbol
           
            param: chainType
            type: str
            description: put, call, or callput
            Default: callput
           
            param: priceType
            type: 'atmn', 'all', None
            description: The price type
            Default: ATNM
           
            param: expiry_date
            type: dt.date()
            description: contract expiration date; if expiry_date is None, then gets the expiration_date closest to today
           
            param: optionCategory
            type: 'standard', 'all', 'mini', None
            description: what type of option data to return
            Default: standard
           
            param: skipAdjusted
            type: bool
            description: Specifies whether to show (TRUE) or not show (FALSE) adjusted options, i.e., options 
                        that have undergone a change resulting in a modification of the option contract.
           
            param: resp_format
            type: 'json', 'xml' or None
            description: Response format json, xml, or None (python object)
           
            Sample Request
            GET https://api.etrade.com/v1/market/optionchains?expirationDay=03&expirationMonth=04&expirationYear=2011&chainType=PUT&skipAdjusted=true&symbol=GOOGL

        '''
        assert resp_format in ('xml', None)
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
            args.append('chainType=%s' % chainType.upper())
        if optionCategory is not None:
            args.append('optionCategory=%s' % optionCategory.upper())
        if priceType is not None:
            args.append('priceType=%s' % priceType.upper())
        if skipAdjusted is not None:
            args.append('skipAdjusted=%s' % str(skipAdjusted))
        if noOfStrikes is not None:
            args.append('noOfStrikes=%d' % noOfStrikes.upper())
        api_url = self.base_url + 'optionchains?' + '&'.join(args)
        
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(api_url)
        LOGGER.debug(req.text)

        if resp_format=='xml':
            return req.text
        else:
            try:
                root = ET.fromstring(req.text)
            except:
                raise
            
# should be put and calls in the OptionPair leafs; just in case, expect one, and not the second
            rtn = list()
            for pair in root.findall('OptionPair'):
                for a in pair.getchildren():
                    b = {i.tag:i.text for i in a.getchildren() }
                    for x in ('timeStamp','volume','askSize','bidSize','openInterest'): b[x] = int(b[x])
                    for x in ('bid','ask','strikePrice','netChange','lastPrice'): b[x] = float(b[x])
                    greeks = dict()
                    for i in a.find('OptionGreeks'):
                        try:
                            greeks[i.tag] = float(i.text)
                        except:
                            pass
                    b['OptionGreeks'] = greeks
                    rtn.append(b)
            return rtn

    def get_option_expire_date(self, underlier, resp_format=None):
        ''' get_option_expiry_dates(underlier, resp_format=None)
        
            If resp_format is None, return a list of datetime.date objects for the underlier, as returned by the Etrade API.
            Otherwise, return the XML or JSON text as appropriate for resp_format.
            
            JSON formatted return does not work as documented.
            However, the XML formatted response correctly returns the weekly and monthly option dates
            
            param: underlier
            type: str
            description: market symbol
           
            param: resp_format
            type: 'json', 'xml' or None
            description: Response format json, xml, or None (python object)
           
            https://api.etrade.com/v1/market/optionexpiredate?symbol={symbol}
                
            Sample Request
            GET https://api.etrade.com/v1/market/optionexpiredate?symbol=GOOG&expiryType=ALL
            
            XML response: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><OptionExpireDateResponse><ExpirationDate><year>2012</year><month>11</month><day>23</day><expiryType>WEEKLY</expiryType></ExpirationDate><ExpirationDate><year>2012</year><month>12</month><day>22</day><expiryType>MONTHLY</expiryType></ExpirationDate><ExpirationDate><year>2013</year><month>1</month><day>19</day><expiryType>MONTHLY</expiryType></ExpirationDate><ExpirationDate><year>2013</year><month>3</month><day>16</day><expiryType>MONTHLY</expiryType></ExpirationDate><ExpirationDate><year>2013</year><month>6</month><day>22</day></ExpirationDate><ExpirationDate><year>2014</year><month>1</month><day>18</day><expiryType>MONTHLY</expiryType></ExpirationDate><ExpirationDate><year>2015</year><month>1</month><day>17</day><expiryType>DAILY</expiryType></ExpirationDate></OptionExpireDateResponse>'
            
            another way to do this is with lxml:
                import lxml.etree as etree
                r = etree.parse(xml).getroot()
                date_list = list()
                for this_one in r:
                    q = {a.tag: a.text for a in this_one.getchildren()}
                    date_list.append(dt.date(int(q['year']), int(q['month']), int(q['day'])))
        '''

        assert resp_format in (None,'xml')
        api_url = self.base_url + 'optionexpiredate?symbol=%s&expiryType=ALL' % underlier
        LOGGER.debug(api_url)
        
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)
        
        if resp_format=='xml':
            return req.text
        else:
            dates = list()
            try:
                root = ET.fromstring(req.text)
            except Exception as err:
                LOGGER.error(err)
                raise
            for a in root.findall('ExpirationDate'):
                this_date = { i.tag: i.text for i in a.getchildren() }
                dates.append(dt.date(int(this_date['year']), int(this_date['month']), int(this_date['day'])))
            return dates
    