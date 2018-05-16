#!/usr/bin/python3

'''Market - ETrade Market API
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
    
    option_dates = me.get_optionexpiredate('aapl', resp_format=None )
    strikes = me.get_option_strikes('aapl', 5, 2018)
    option_data = me.get_option_chain_data('aapl',strikes)
    
    or, all in one:
    (option_data,count) = me.get_all_option_data('aapl')

'''

import logging
import jxmlease
import datetime as dt
from requests_oauthlib import OAuth1Session

# Set up logging
LOGGER = logging.getLogger(__name__)

# know when today is
TODAY = dt.date.today()
(THIS_YEAR, THIS_MONTH, THIS_DAY) = (TODAY.year, TODAY.month, TODAY.day)

        
def decode_option_xml(xml_text):
    ''' given xml_text, return list of option chains
        return list of (dt.date,strikePrice) tuples
        {'call': {'expireDate': {'day': '18',
                      'expiryType': 'MONTHLY',
                      'month': '5',
                      'year': '2018'},
       'product': {'exchangeCode': 'CINC',
                   'symbol': "AAPL May 18 '18 $250 Call",
                   'typeCode': 'OPTN'},
       'rootSymbol': 'AAPL',
       'strikePrice': '250.000000'},
    '''
    xmlobj = jxmlease.parse(xml_text)
    z = xmlobj['OptionChainResponse']['optionPairs']
    
# determine whether call or put from first item in list
    if 'call' in z[0]:
        option_type = 'call'
    else:
        option_type = 'put'
        
    x = list()
    for this_opt in z:
        q = this_opt[option_type]['expireDate']
        strikePrice = float(this_opt[option_type]['strikePrice'])
        x.append((dt.date(int(q['year']),int(q['month']),int(q['day'])),strikePrice))        
    return x
    

class ETradeMarket(object):
    '''ETradeMarket'''
    def __init__(self, client_key, client_secret,
                 resource_owner_key, resource_owner_secret, dev=True):
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
           description: OAuth authentication token secret
           param: dev
           type: boolean
           description: use the development environment (True) or production (False)
        '''
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.dev_environment = dev
        self.base_url = (r'https://etwssandbox.etrade.com' if dev else r'https://etws.etrade.com')
        self.session = OAuth1Session(self.client_key,
                                     self.client_secret,
                                     self.resource_owner_key,
                                     self.resource_owner_secret,
                                     signature_type='AUTH_HEADER')

    def look_up_product(self, company, s_type, resp_format='json'):
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
        uri = (r'market/sandbox/rest/productlookup' if self.dev_environment else  r'market/rest/productlookup')
        api_url = '%s/%s' % (self.base_url, uri)
        if resp_format == 'json':
            api_url = api_url + '.json'
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

    def get_quote(self, args, resp_format='json', detail_flag='ALL'):
        '''get_quote(dev, resp_format, **kwargs) -> resp
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
           type: list
           required: true
           description: One or more symobols
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
                
                y=self.get_quote(['googl','aapl'])
                y['quoteResponse']['quoteData'][0]['all'] ==> dictionary for 1st element in return list
                
                y=self.get_quote(['AAPL:2018:05:18:put:150'])
            '''
            
        # ensure that a max of 25 symbols are sent
        args_25 = ','.join(args[:25])
        uri = (r'market/sandbox/rest/quote/' if self.dev_environment else r'market/rest/quote/')
        api_url = '%s/%s%s' % (self.base_url, uri, args_25)
        if resp_format == 'json': api_url += '.json'
        
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
        
    def get_all_option_data(self, underlier):
        ''' Given the underlier, return all option_chain_data as a dictionary of lists,
            with the key being a text date of the form YYYY-MM; e.g., 2018-05
            INPUT: underlying symbol
            RETURN: dictionary of lists
                    count of total options downloaded
        '''
        expiry_dates = self.get_optionexpiredate(underlier)     # this contains all expiration dates
        
        # group by month, as this is the approach that ETrade API returns options_chain_data
        rtn = dict()
        count = 0
        for this_date in expiry_dates:
            option_key = '%04d-%02d' % (this_date.year, this_date.month)
            if option_key not in rtn:
                strikes = self.get_option_strikes(underlier, this_date.month, this_date.year)
                rtn[option_key] = self.get_option_chain_data('aapl',strikes)
                count += len(rtn[option_key])
        
        return rtn, count
        
    def get_option_chain_data(self, underlier, date_strikes):
        ''' Return a list of dictionary objects, one for each option_chain entry
            INPUT:  underlier: a particular symbol
                    date_strikes is a dictionary with two keys ('put','call') that each
                            contains a list of (dt.dates, strike_price) tuples
            RETURN: list of dictionary objects with all the option data in it
            
            for each option, get_quote using format underlier:year:month:day:optionType:strikePrice.
            Package the requests up in groups of 25 to limit number of calls to Etrade API.
        '''
        assert 'put' in date_strikes
        assert 'call' in date_strikes
        
        # create request strings
        reqs = list()
        for opt_type in ('put','call'):
            for (this_dt,this_strike) in date_strikes[opt_type]:
                reqs.append('%s:%04d:%02d:%02d:%s:%.2f' % (underlier, this_dt.year, this_dt.month, this_dt.day,
                                                           opt_type, this_strike))
        
        # send off requests in batches of 25; add to return list
        rtn = list()
        for n in range(0,len(reqs),25):
            x = self.get_quote(reqs[n:n+25])
            y = x['quoteResponse']['quoteData']
            if isinstance(y,dict):
                rtn.append(y)
            elif isinstance(y,list):
                rtn += y
            else:
                LOGGER.error('Return from get_quote not expected; got %s', x)
        return rtn
    
    def get_option_strikes(self, underlier, expirationMonth=THIS_MONTH, expirationYear=THIS_YEAR):
        ''' Return all put and call dates and strikes as a dictionary.
        
            INPUT: underlier: a particular symbol
                   expirationMonth, expirationYear: integers
                   dev: true or false (production)
            RETURN: dictionary with keys('put','call'), each of which has a list of (dt.dates, strike_price) tuples
        '''
        assert 0 < expirationMonth <= 12
        assert expirationYear >= 2010
        date_strikes = dict()
        for opt_type in ('put','call'):
            xml_text = self.get_optionchains(underlier, expirationMonth, expirationYear, chainType=opt_type, resp_format=None)
            date_strikes[opt_type] = decode_option_xml(xml_text)
            
        return date_strikes
    
    def get_optionchains(self, underlier, expirationMonth=THIS_MONTH, expirationYear=THIS_YEAR, skipAdjusted=True,
                         chainType='callput', resp_format=None):
        '''get_optionchains(dev, resp_format, **kwargs) -> resp
        
           param: underlier
           type: str
           description: market symbol
           
           param: chainType
           type: str
           description: PUT, CALL, or CALLPUT
           
           param: expirationMonth
           type: int
           description: contract expiration month; number between 1 (January) and 12 (December)
           
           param: expirationYear
           type: int
           description: contract expiration year; number between 2012 and future year
           
           param: skipAdjusted
           type: bool
           description: Specifies whether to show (TRUE) or not show (FALSE) adjusted options, i.e., options 
                        that have undergone a change resulting in a modification of the option contract.
           
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           
           Sample Request
           GET https://etws.etrade.com/market/rest/optionchains?expirationMonth=04&expirationYear=2011&chainType=PUT&skipAdjusted=true&underlier=GOOG

        '''
        assert 0 < expirationMonth <= 12
        assert expirationYear >= 2010
        assert (resp_format in ('json', None))
        assert chainType in ('put', 'call', 'callput')
        
        args_str = 'expirationMonth=%02d&expirationYear=%04d&underlier=%s&skipAdjusted=%s&chainType=%s' % (expirationMonth,
                                                                expirationYear, underlier, str(skipAdjusted), chainType.upper())
        
        uri = (r'market/sandbox/rest/optionchains' if self.dev_environment else r'market/rest/optionchains')
        api_url = '%s/%s?%s' % (self.base_url, uri, args_str)
        
        if resp_format == 'json':
            req = self.session.get(api_url + '.json')
        else:
            req = self.session.get(api_url)
        LOGGER.debug(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json()
        else:
            return(req.text)  

    def get_optionexpiredate(self, underlier, resp_format=None):
        '''get_option_expiry_dates(dev, resp_format, **kwargs) -> resp
        
            if resp_format is None, return a list of datetime.date objects, which seem to be
            sorted in ascending order.
            
            if resp_format is 'json', return the python object <== this currently doesn't work
            
           param: underlier
           type: str
           description: market symbol
           
           param: dev
           type: bool
           description: API enviornment
           
           param: resp_format
           type: str
           description: Response format .JSON or None = XML
           
           Sample Request
           GET https://etws.etrade.com/market/rest/optionexpiredate?underlier=GOOGL
           or  https://etws.etrade.com/market/rest/optionexpiredate?underlier=GOOGL.json  <== doesn't seem to work
        '''

        args_str = 'underlier=%s' % underlier
        uri = (r'market/sandbox/rest/optionexpiredate' if self.dev_environment else r'market/rest/optionexpiredate')
        api_url = '%s/%s?%s' % (self.base_url, uri, args_str)
        LOGGER.debug(api_url)
        
        if resp_format == 'json':
            req = self.session.get(api_url + '.json')
        else:
            req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

# JSON format a lot easier to deal with, but doesn't seem to work
        if resp_format == 'json':
            return req.json()
        else:
            try:
                xmlobj = jxmlease.parse(req.text)
                z = xmlobj['OptionExpireDateGetResponse']['ExpirationDate']
                dates = [ dt.date(int(this_date['year']), int(this_date['month']), int(this_date['day'])) for this_date in z ]
            except Exception as err:
                LOGGER.error(err)
                return None
            return dates
        