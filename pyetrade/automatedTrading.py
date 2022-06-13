import ast
import json
import configparser
import requests
from rauth import OAuth1Service
import time

# not needed from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

import pandas as pd
import random

# loading configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Global lists
# List of stocks to buy or short based on MACD and RSI numbers
stockBuy = []
stockShort = []
# List for the stocks that did not meet the trade parameters
watchList = []


_SLEEP_SECOND_N = 3

def get_authorize_code(authorize_url):
    #############################################
    # Automate the login process
    options = Options()
    options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path="/usr/bin/firefox")
    # driver = webdriver.Chrome(executable_path="/usr/bin/google-chrome", options=options)
    driver = webdriver.Chrome(config["DEFAULT"]["CHROMEDRIVER"], options=options)

    driver.get(authorize_url)
    cookie = ast.literal_eval(config["DEFAULT"]["COOKIE"])
    driver.add_cookie(cookie)
    
    userid = driver.find_element_by_id("user_orig")
    userid.send_keys(config["DEFAULT"]["USERNAME"])
    time.sleep(_SLEEP_SECOND_N)

    passwd = driver.find_element_by_css_selector("input[type='password']")
    passwd.send_keys(config["DEFAULT"]["PASSWORD"] + "\n")
    time.sleep(_SLEEP_SECOND_N)

    '''
    logon = driver.find_element_by_id("logon_button")
    logon.click()
    time.sleep(_SLEEP_SECOND_N)
    '''
    
    driver.implicitly_wait(5)
     
    accept = driver.find_element_by_xpath("//form[@name='CustInfo']/input[3]")
    accept.click()
    
    code = driver.find_element_by_xpath("//div[@style='text-align:center']/input[1]")
    code = code.get_attribute('value')
    
    driver.close()
    return code
        

# Read config file
# login and authenticate
def oauth():
    """Allows user authorization for the sample application with OAuth 1"""
    etrade = OAuth1Service(
        name="etrade",
        consumer_key=config["DEFAULT"]["CONSUMER_KEY"],
        consumer_secret=config["DEFAULT"]["CONSUMER_SECRET"],
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com")
    
    base_url = config["DEFAULT"]["PROD_BASE_URL"]
    
     # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"})

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a text code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    print(authorize_url)
    
    text_code = get_authorize_code(authorize_url)
    print(text_code)

    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={"oauth_verifier": text_code})
    
    print(session)
    # automateTrades(session, base_url)
        
# Trade the stocks automatically based on MACD and RSI
def automateTrades(session, base_url):
    
    stockAnalysis()
    
    # Get account
    account = getAccount(session, base_url)
    
    # Test
    orderType = "BUY"
    stock = "SNAP"
    order = createOrder(stock, orderType)
    previewOrder(order, session, account, base_url)
    
    # Create buy orders 
   # for stock in stockBuy:
       # orderType = "BUY"
       # order = createOrder(stock, orderType)
       # placeOrder(order, session, account, base_url)
    
    # Create short orders
    #for stock in stockShort:
      #  orderType = "SELL_SHORT"
       # order = createOrder(stock, orderType)
       # placeOrder(order, session, account, base_url)
        
# read MACD/ RSI file to determine trades
def stockAnalysis():
    
    stockData = pd.read_csv("")
    
    global stockBuy, stockShort, watchList
    
    for index, stocks in stockData.iterrows():
        
        if(stocks['MACD'] == 1 and stocks['RSI'] > 70):
            stockShort.append(stocks['Symbol'])
       
        elif(stocks['MACD'] == -1 and stocks['RSI'] < 30):
            stockBuy.append(stocks['Symbol'])
        
        else:
            watchList.append(stocks['Symbol'])
        
# Get account information
def getAccount(session, base_url):
    
    # URL for the API endpoint
    url = base_url + "/v1/accounts/list.json"
    
    # Make API call for GET request
    response = session.get(url, header_auth=True)
    
    if response is not None and response.status_code == 200:

        data = response.json()
        
        if data is not None and "AccountListResponse" in data and "Accounts" in data["AccountListResponse"] \
                    and "Account" in data["AccountListResponse"]["Accounts"]:
                accounts = data["AccountListResponse"]["Accounts"]["Account"]
                
                # Get the first account in the list of accounts
                account = accounts[0]
                
    return account

# create order template
def createOrder(stock, orderType):
     
     order = {"price_type": "MARKET",
                 "order_term": "GOOD_FOR_DAY",
                 "symbol": "",
                 "order_action": "",
                 "limit_price":"",
                 "quantity": "1"}
     
     
     order['symbol'] = stock
     order['order_action'] = orderType
     order['limit_price'] = None
     order["client_order_id"] = random.randint(1000000000, 9999999999)
     
     return order
 
def previewOrder(order, session, account, base_url):
    # URL for the API endpoint
    url = base_url + "/v1/accounts/" + account["accountIdKey"] + "/orders/preview.json"

    # Add parameters and header information
    headers = {"Content-Type": "application/xml", "consumerKey": config["DEFAULT"]["CONSUMER_KEY"]}

    # Add payload for POST Request
    payload = """<PlaceOrderRequest>
                    <orderType>EQ</orderType>
                    <clientOrderId>{0}</clientOrderId>
                    <Order>
                        <allOrNone>false</allOrNone>
                        <priceType>{1}</priceType>
                        <orderTerm>{2}</orderTerm>
                        <marketSession>REGULAR</marketSession>
                        <stopPrice></stopPrice>
                        <limitPrice>{3}</limitPrice>
                        <Instrument>
                            <Product>
                                <securityType>EQ</securityType>
                                <symbol>{4}</symbol>
                            </Product>
                            <orderAction>{5}</orderAction>
                            <quantityType>QUANTITY</quantityType>
                            <quantity>{6}</quantity>
                        </Instrument>
                    </Order>
                </PlaceOrderRequest>"""
    payload = payload.format(order["client_order_id"], order["price_type"], order["order_term"],
                                 order["limit_price"], order["symbol"], order["order_action"], order["quantity"])
    
    # Make API call for POST request
    response = session.post(url, header_auth=True, headers=headers, data=payload)
    
    if response is not None and response.status_code == 200:
            data = response.json()
            print("\nPreview Order:")
            print(data)
    else:
            # Handle errors
            data = response.json()
            if 'Error' in data and 'message' in data["Error"] and data["Error"]["message"] is not None:
                print("Error: " + data["Error"]["message"])
                print(data)
            else:
                print("Error: Preview Order API service error")
                print(data)

# Make orders from order template
def placeOrder(order, session, account, base_url):
    
    # URL for the API endpoint
    url = base_url + "/v1/accounts/" + account["accountIdKey"] + "/orders/place"

   # Todo

# Create report of trades 

if __name__ == "__main__":
    oauth()
