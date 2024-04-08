# pyetrade (Python E-Trade API Wrapper)

[![PyPI](https://img.shields.io/pypi/v/pyetrade.svg)](https://pypi.python.org/pypi/pyetrade)
[![PyPI](https://img.shields.io/pypi/l/pyetrade.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/pyetrade.svg)](https://pypi.python.org/pypi/pyetrade)
[![Build Status](https://github.com/jessecooper/pyetrade/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/jessecooper/pyetrade/actions/workflows/build.yml/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/jessecooper/pyetrade/branch/master/graph/badge.svg)](https://codecov.io/gh/jessecooper/pyetrade)

## Completed

* Authorization API - ALL (OAuth)
  * get_request_token
  * get_access_token
  * renew_access_token
  * revoke_access_token

* Alerts API
  * list_alerts
  * list_alert_details
  * delete_alert

* Accounts API
  * list_accounts
  * get_account_balance
  * get_account_portfolio
  * get_portfolio_position_lot
  * list_transactions
  * list_transaction_details

* Order API
  * list_orders
  * find_option_orders
  * preview_equity_order
  * change_preview_equity_order
  * place_equity_order
  * place_changed_equity_order
  * place_option_order
  * place_changed_option_order
  * cancel_order

* Market API
  * look_up_product
  * get_quote
  * get_option_chains
  * get_option_expire_date

## Install

```bash
pip install pyetrade
```
OR
```bash
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

[ETrade API Docs](https://apisb.etrade.com/docs/api/account/api-account-v1.html)

### Development Setup:

* Fork pyetrade
* Setup development environment

```bash
make init
make devel
```
OR
```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -e .
pre-commit install --hook-type pre-commit --hook-type pre-push
```

* Lint (Run analysis - pre-commit-config)

```bash
make analysis
```

* Test (Coverage >= 90%)

```bash
make test
```

* Push Changes
  * Push changes to a branch on your forked repo


* Create pull request
  * Open a pull request on pyetrade and put your fork as the source of your changes
