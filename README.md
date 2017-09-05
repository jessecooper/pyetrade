# pyetrade

Python E-Trade API Wrapper   
[![PyPI](https://img.shields.io/pypi/v/pyetrade.svg)](https://pypi.python.org/pypi/pyetrade)
[![PyPI](https://img.shields.io/pypi/l/pyetrade.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/pyetrade.svg)](https://pypi.python.org/pypi/pyetrade)
[![Build Status](https://travis-ci.org/jessecooper/pyetrade.svg?branch=master)](https://travis-ci.org/jessecooper/pyetrade)
[![codecov](https://codecov.io/gh/jessecooper/pyetrade/branch/master/graph/badge.svg)](https://codecov.io/gh/jessecooper/pyetrade)
## Completed
Authorization API - ALL  
Accounts API - 
* List Accounts 
* Get Account Ballance 
* Get Account Positions 
 
Order API - 
* List Orders
* Place Equity Order 
 
Market API - 
* Look Up Product 
* Get Quote  

## TODO
Accounts API - See pyetrade/accounts.py  
Order API - See pyetrade/order.py  
Market API - See pyetrade/market.py  
Notification API - ALL  
Limits API - ALL  

## Install
```
pip install pyetrade
- or -
git clone https://github.com/jessecooper/pyetrade.git
cd pyetrade
sudo make init
sudo make install
```
## Example Usage
```python
import pyetrade
oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
oauth.get_request_token()
#Follow url and get verification code
tokens = oauth.get_access_token(verifier_code)
accounts = pyetrade.ETradeAccounts(
        consumer_key,
        consumer_secret, 
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )
accounts.list_accounts()
```
## Documentation
[PyEtrade Documentation](https://pyetrade.readthedocs.io/en/latest/)
## Contribute to pyetrade
* [ETrade API Docs](https://developer.etrade.com/ctnt/dev-portal/getArticleByCategory?category=Documentation)
* Fork pyetrade
* Development Setup:  
```
    sudo make init  
    sudo make devel
```
* Lint  
```
make lint #Lint score should be >=8
```
* Test  
```
make test #Ensure test coverage is >80%
```
* Push Changes:  
Push changes to a branch on your forked repo
* Create pull request
