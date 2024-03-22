# pyetrade

Python E-Trade API Wrapper
[![PyPI](https://img.shields.io/pypi/v/pyetrade.svg)](https://pypi.python.org/pypi/pyetrade)
[![PyPI](https://img.shields.io/pypi/l/pyetrade.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/pyetrade.svg)](https://pypi.python.org/pypi/pyetrade)
[![Build Status](https://github.com/jessecooper/pyetrade/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/jessecooper/pyetrade/actions/workflows/build.yml/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/jessecooper/pyetrade/branch/master/graph/badge.svg)](https://codecov.io/gh/jessecooper/pyetrade)

## Completed
v1 API
Authorization API - ALL
Accounts
* list accounts

Authorization API - ALL
Order API -
* List Orders
* Place Equity Order
* Cancel Order

Market API -
* Look Up Product
* optionchain
* Get Quote

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

To create the OAuth tokens:
```python
import pyetrade

consumer_key = "<CONSUMER_KEY>"
consumer_secret = "<SECRET_KEY>"

oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
print(oauth.get_request_token())  # Use the printed URL

verifier_code = input("Enter verification code: ")
tokens = oauth.get_access_token(verifier_code)
print(tokens)
```

And then on the example code:

```python
import pyetrade

consumer_key = "<CONSUMER_KEY>"
consumer_secret = "<SECRET_KEY>"
tokens = {'oauth_token': '<TOKEN FROM THE SCRIPT ABOVE>',
          'oauth_token_secret': '<TOKEN FROM THE SCRIPT ABOVE>'}

accounts = pyetrade.ETradeAccounts(
    consumer_key,
    consumer_secret,
    tokens['oauth_token'],
    tokens['oauth_token_secret']
)

print(accounts.list_accounts())
```
## Documentation
[PyEtrade Documentation](https://pyetrade.readthedocs.io/en/latest/)
## Contribute to pyetrade
* [ETrade API Docs](https://apisb.etrade.com/docs/api/account/api-account-v1.html)
* Fork pyetrade
* Development Setup:
```
    make init
    make devel
```
or
```
    pip install -r requirements.txt
    pip install -r requirements_dev.txt
    pip install -e .
```
* Lint
```
# Run Black
black pyetrade/
# Run Linter
pylint pyetrade/  #Lint score should be >=8
```
* Test
```
make test #Ensure test coverage is >80%
```
* Push Changes:
Push changes to a branch on your forked repo
* Create pull request
