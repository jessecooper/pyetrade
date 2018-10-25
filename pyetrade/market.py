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
    
    option_dates = me.get_option_expire_date('aapl', None)
    strikes = me.get_option_strikes('aapl', 2018, 10, 12)
    option_data = me.get_option_chain_data('aapl',strikes)
    
    or, all in one get all strikes for all future dates:
    (option_data,count) = me.get_all_option_data('aapl')

'''

import logging
import jxmlease
import datetime as dt
import dateutil.parser
from requests_oauthlib import OAuth1Session

LOGGER = logging.getLogger(__name__)
TODAY = dt.date.today()
(THIS_YEAR, THIS_MONTH, THIS_DAY) = (TODAY.year, TODAY.month, TODAY.day)
if TODAY.weekday()<=4:              # before Friday
    days_to_Friday = 4 - TODAY.weekday()
else:                               # after Friday
    days_to_Friday = 11 - TODAY.weekday()
NEXT_FRIDAY = TODAY + dt.timedelta(days=days_to_Friday)
        
def strikes_from_optionchains_XML(xml_text):
    ''' strikes_from_optionchains_XML(xml_text)
    
        Given xml_text from an option chains download, return list of option chain dates and strikes
        return list of (dt.date,strikePrice) tuples
        
        { 'call': {'expireDate': {'day': '18',
                   'expiryType': 'MONTHLY',
                   'month': '5',
                   'year': '2018'},
          'product': {'exchangeCode': 'CINC',
                      'symbol': "AAPL May 18 '18 $250 Call",
                      'typeCode': 'OPTN'},
          'rootSymbol': 'AAPL',
          'strikePrice': '250.000000'
        }
          
    '''
    rtn = list()
    try:
        xmlobj = jxmlease.parse(xml_text)
        z = xmlobj['OptionChainResponse']['optionPairs']
    except:
        return rtn
    
# determine whether call or put from first item in list
    if 'call' in z[0]:
        option_type = 'call'
    else:
        option_type = 'put'
        
    rtn = [ float(this_opt[option_type]['strikePrice']) for this_opt in z ]    
    return rtn

def settlement_datetime(opt):
    ''' Extract the datetime the option data was acquired.
        This is simply a helper function.
    '''
    try:
        return dateutil.parser.parse(opt['all']['askTime'],ignoretz=True)
    except:
        raise

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
        
    def __str__(self):
        ret = [ 'symbol: %s' % self.symbol,
                'Use development environment: %s' % self.dev_environment,
                'base URL: %s' % self.base_url
                ]
        return '\n'.join(ret)

    def look_up_product(self, company, s_type, resp_format='json'):
        '''look_up_product(company, s_type, resp_format='json')
        
           param: company
           type: string
           description: full or partial name of the company. Note
           that the system extensivly abbreviates common words
           such as company, industry and systems and generally
           skips punctuation
           
           param: s_type. possible values are:
               * EQ (equity)
               * MF (mutual fund)
           type: enum
           description: the type of security.
               
           param: companyName
           type: string
           description: the company name
           
           param: exhange
           type: string
           description: the exchange that lists that company
           
           param: securityType
           type: string
           description: the type of security. EQ or MF
           
           param: symbol
           type: string
           description: the market symbol for the security
           
           '''
           
        assert resp_format in ('json','xml')
        uri = (r'market/sandbox/rest/productlookup' if self.dev_environment else r'market/rest/productlookup')
        api_url = '%s/%s.%s' % (self.base_url, uri, resp_format)
        LOGGER.debug(api_url)
        
        #add detail flag to url
        payload = { 'company': company, 'type': s_type }
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json()
        else:
            return req.text

    def get_quote(self, args, resp_format='json', detail_flag='ALL'):
        ''' get_quote(resp_format, detail_flag, **kwargs)
        
            Get quote data on all symbols provided in the list args.
            the eTrade API is limited to 25 requests per call. Issue
            warning if more than 25 are requested. Only process the first 25.
        
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
            
        assert resp_format in ('json','xml')
        assert isinstance(args,list)
        if len(args) > 25: LOGGER.warning('get_quote asked for %d requests; only first 25 returned' % len(args))
        
        args_str = ','.join(args[:25])       # ensure that a max of 25 symbols are sent
        uri = (r'market/sandbox/rest/quote/' if self.dev_environment else r'market/rest/quote/')
        api_url = '%s/%s%s' % (self.base_url, uri, args_str)
        if resp_format == 'json': api_url += '.json'
        
        LOGGER.debug(api_url)
        payload = {'detailFlag': detail_flag}
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json()
        else:
            return req.text
        
    def get_all_option_data(self, underlier, verbose=False):
        ''' get_all_option_data(underlier, verbose=False)
        
            Given the underling symbol, return all option_chain_data as a dictionary of lists
            and the total count options chains returned
            
            INPUT:
                * underlying symbol
            
            RETURN
                * dictionary of lists (the dictionary key is the option_expiry dt.date)
                * total count of options downloaded
                
        '''
        try:
            expiry_dates = self.get_option_expire_date(underlier, resp_format=None)     # this contains all expiration dates for the underlier
        except Exception as err:
            LOGGER.error(err)
            raise

        rtn = dict()
        count = 0
        for this_date in expiry_dates:
            strikes = self.get_option_strikes(underlier, this_date)
            if len(strikes['put']):
                rtn[this_date] = self.get_option_chain_data(underlier,this_date,strikes)
                count += len(rtn[this_date])
                if verbose: print('downloaded %d options for expiry %s' % (len(rtn[this_date]),str(this_date) ))
        return rtn, count
        
    def get_option_chain_data(self, underlier, expiry_date, strikes):
        ''' get_option_chain_data(underlier, date_strikes)
            
            Return a list of dictionary objects, one for each option_chain entry for the underlier
            
            INPUT:
                * underlier: a particular symbol
                * expiry_date: a particular expiry date
                * strikes is a dictionary with two keys ('put','call') that each
                            contains a list of strike_price
            RETURN:
                * list of dictionary objects with all the option data in it
            
            For each option, get_quote using format underlier:year:month:day:optionType:strikePrice.
            Package the requests up in groups of 25 to minimize the number of Etrade API calls.
            Create a list of dictionary objects to return based on the requests.
            
        '''
        assert 'put' in strikes
        assert 'call' in strikes
        
        # create request strings
        reqs = list()
        for opt_type in ('put','call'):
            for this_strike in strikes[opt_type]:
                reqs.append('%s:%04d:%02d:%02d:%s:%.2f' % (underlier, expiry_date.year, expiry_date.month, expiry_date.day,
                                                           opt_type, this_strike))
        
        # send off requests in batches of 25; add to return list
        rtn = list()
        for n in range(0,len(reqs),25):
            try:
                x = self.get_quote(reqs[n:n+25])
                y = x['quoteResponse']['quoteData']
            except Exception as err:
                LOGGER.error('underlier %s expiry date %s failed', underlier.upper(), str(expiry_date))
                continue
            if isinstance(y,dict):
                rtn.append(y)
            elif isinstance(y,list):
                rtn += y
            else:
                LOGGER.error('Return from get_quote not expected; got %s', x)
        return rtn
    
    def get_option_strikes(self, underlier, expiry_date):
        ''' get_option_strikes(underlier, expiry_date)
        
            Return a dictionary with a list of puts and a list of call option tuples. Each tuple contains
            the date and strike price. If an invalid date is passed (one that has no options), then
            that particular date with have no entries (0 length list).
        
            INPUT:
                * underlier: a particular symbol
                * expiry_date: the dt.date of contract expiration
                
            RETURN:
                * dictionary with keys('put','call'), each of which has a list of strike_price
                
        '''
        assert expiry_date.year >= 2010
        strikes = dict.fromkeys(('put','call'), list())
        for opt_type in ('put','call'):
            try:
                xml_text = self.get_optionchains(underlier, expiry_date, chainType=opt_type)
                strikes[opt_type] = strikes_from_optionchains_XML(xml_text)
            except:             # fails get_optionchains if options don't exist for year-month-day
                pass
            
        return strikes
    
    def get_optionchains(self, underlier, expiry_date, skipAdjusted=True, chainType='callput', resp_format=None):
        '''get_optionchains(underlier, expiry_date, skipAdjusted=True, chainType='callput', resp_format=None)
        
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
           description: Response format JSON or None = XML
           
           Sample Request
           GET https://etws.etrade.com/market/rest/optionchains?expirationMonth=04&expirationYear=2011&chainType=PUT&skipAdjusted=true&underlier=GOOG

        '''
        assert expiry_date.year >= 2010
        assert (resp_format in ('json', None))
        assert chainType in ('put', 'call', 'callput')
        
        args_str = 'expirationDay=%02d&expirationMonth=%02d&expirationYear=%04d&underlier=%s&skipAdjusted=%s&chainType=%s' % (expiry_date.day,
                    expiry_date.month, expiry_date.year, underlier, str(skipAdjusted), chainType.upper())
        
        uri = (r'market/sandbox/rest/optionchains' if self.dev_environment else r'market/rest/optionchains')
        api_url = '%s/%s?%s' % (self.base_url, uri, args_str)
        
        if resp_format == 'json':
            req = self.session.get(api_url + '.json')
        else:
            req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(api_url)
        LOGGER.debug(req.text)

        if resp_format == 'json':
            return req.json()
        else:
            return(req.text)  

    def get_option_expire_date(self, underlier, resp_format=None):
        ''' get_option_expiry_dates(underlier, resp_format, **kwargs)
        
            Return a sorted list of datetime.date objects for the underlier. Some of the returned dates may not actually
            have any options.
            
            if resp_format is 'json', return the python object <== this currently doesn't work as described by the eTrade API
            
            Another problem is the etrade API only returns monthlies, not weeklies. Therefore, invent some weeklies which occur on Fridays
            for the present month and one month out, generally. These may not exist, but there is no way to know without asking
            for option_chain data and getting a NULL response.
            
            param: underlier
            type: str
            description: market symbol
           
            param: resp_format
            type: str
            description: Response format .JSON or None = XML
           
            Sample Request
            GET https://etws.etrade.com/market/rest/optionexpiredate?underlier=GOOGL
            or  https://etws.etrade.com/market/rest/optionexpiredate?underlier=GOOGL.json  <== doesn't seem to work
            
        '''

        assert resp_format in (None,'json','xml')
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
                raise

# add weeklies for this month and the following month
        friday = NEXT_FRIDAY
        for i in range(8):
            if friday not in dates: dates.append(friday)
            friday += dt.timedelta(days=7)
        
        return sorted(dates)
    