PyEtrade Examples
==================

PyEtrade examples for some of the modules are as below

Important requirements
-----------------------

Getting access tokens requires the users `Consumer key` and `Consumer Secret`
obtained from E*TRADE. This applies equally to both the sandbox and Live
environments.

For the sandbox key, request a Sandbox consumer key via
`<https://us.etrade.com/etx/ris/apikey>`_ and for the Live/Production environment,
request a key through the E*TRADE secure message. Please refer
`E*TRADE Developer <https://developer.etrade.com/getting-started>`_ for
more information

The following examples assume you were successfully able to obtain the
`Consumer key` and `Consumer Secret` from E*TRADE.

Primary Authorization
----------------------

0.  Creating tokens (This step is required before performing any action
    on Etrade via PyEtrade

.. code-block:: python

    # Importing the pyetrade module
    import pyetrade

    # Obtained secrets from Etrade for Sandbox or Live
    consumer_key = "<CONSUMER_KEY>"
    consumer_secret = "<SECRET_KEY>"

    # Using the EtradeOAuth object to retrive the URL to request tokens
    oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
    print(oauth.get_request_token())  # Use the printed URL

    # Use the printed URL to retrive Verification code
    verifier_code = input("Enter verification code: ")
    tokens = oauth.get_access_token(verifier_code)
    print(tokens)


Access Management
------------------

0.  Renewing access tokens

.. code-block:: python

    # Importing the pyetrade module
    import pyetrade

    # Obtained secrets from Etrade for Sandbox or Live
    consumer_key = "<CONSUMER_KEY>"
    consumer_secret = "<SECRET_KEY>"

    # Generated token from Step 0.
    tokens = {'oauth_token': '<TOKEN FROM THE SCRIPT ABOVE>',
              'oauth_token_secret': '<TOKEN FROM THE SCRIPT ABOVE>'}

    # Setting up the object used for Access Management
    authManager = pyetrade.authorization.ETradeAccessManager(
        consumer_key,
        consumer_secret,
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )

    # Triggering a renew
    authManager.renew_access_token()

    # Triggering a Revoke
    authManager.revoke_access_token()


Accounts Management
--------------------

.. code-block:: python

    # Importing the pyetrade module
    import pyetrade

    # Obtained secrets from Etrade for Sandbox or Live
    consumer_key = "<CONSUMER_KEY>"
    consumer_secret = "<SECRET_KEY>"

    tokens = {'oauth_token': '<TOKEN FROM THE SCRIPT ABOVE>',
              'oauth_token_secret': '<TOKEN FROM THE SCRIPT ABOVE>'}

    # Setting up the object used for Accounts activity
    # Arg dev determines the environment Sandbox (dev=True)
    # or Live/Production (dev=False)
    accounts = pyetrade.ETradeAccounts(
        consumer_key,
        consumer_secret,
        tokens['oauth_token'],
        tokens['oauth_token_secret'],
        dev=True
    )

    # lists all the accounts for
    print(accounts.list_accounts(resp_format='json'))

    # The above produces a json with all the accounts and their
    # respective accountIDKeys

    accountIDKey = '<Key for the chosen account from list_accounts>'

    # Prints account balance
    print(accounts.get_account_balance(accountIDKey, resp_format='json'))

    # Gets account portfolio
    print(accounts.get_account_portfolio(accountIDKey, resp_format='json'))

    # Gets all transactions for an account
    print(accounts.list_transactions(accountIDKey, resp_format='json'))

    # The above produces a json with all the transactions for an account
    # and all their transaction IDs
    transactionID = '<Transaction ID for a specific transaction>'

    # Gets all transaction details for a transaction
    print(accounts.list_transaction_details(accountIDKey, transactionID, resp_format='json'))


Alerts Management
------------------

.. code-block:: python

    # Importing the pyetrade module
    import pyetrade

    # Obtained secrets from Etrade for Sandbox or Live
    consumer_key = "<CONSUMER_KEY>"
    consumer_secret = "<SECRET_KEY>"

    tokens = {'oauth_token': '<TOKEN FROM THE SCRIPT ABOVE>',
              'oauth_token_secret': '<TOKEN FROM THE SCRIPT ABOVE>'}

    # Setting up the object used for alerts activity
    # Arg dev determines the environment Sandbox (dev=True)
    # or Live/Production (dev=False)

    alerts = pyetrade.ETradeAlerts(
        consumer_key,
        consumer_secret,
        tokens['oauth_token'],
        tokens['oauth_token_secret'],
        dev=True
    )

    # Get all alerts
    print(alerts.list_alerts(resp_format='json'))

    # The above produces a json with all the alerts
    # and their alert IDs
    alertID = '<Specific alert ID>'

    # Get alert details
    print(alerts.list_alert_details(alert_id=alertID,  resp_format="json"))

    # Delete alert with ID alertID
    alerts.delete_alert(alert_id=alertID,  resp_format="json")


Market Module
--------------

.. code-block:: python

    # Importing the pyetrade module
    import pyetrade

    # Obtained secrets from Etrade for Sandbox or Live
    consumer_key = "<CONSUMER_KEY>"
    consumer_secret = "<SECRET_KEY>"

    tokens = {'oauth_token': '<TOKEN FROM THE SCRIPT ABOVE>',
              'oauth_token_secret': '<TOKEN FROM THE SCRIPT ABOVE>'}

    # Setting up the object used for alerts activity
    # Arg dev determines the environment Sandbox (dev=True)
    # or Live/Production (dev=False)

    market = pyetrade.ETradeMarket(
        consumer_key,
        consumer_secret,
        tokens['oauth_token'],
        tokens['oauth_token_secret'],
        dev=True
    )

    # Getting products symbol with search string
    print(market.look_up_product('alphabet', resp_format='json'))
    print(market.look_up_product('American', resp_format='json'))

    # Getting market quote
    print(market.get_quote(['GOOG'],resp_format='json'))

    # Getting Options chain with expiry_date=None
    print(market.get_option_chains('GOOG', expiry_date=None, resp_format='json'))


    # Getting Options chain with expiry_date specified with datetime
    import datetime as dt
    datt = dt.datetime(year=2020,month=10, day=16)

    print(market.get_option_chains('GOOG', expiry_date=datt, resp_format='json'))


Order Module
-------------

.. code-block:: python

    # Importing the pyetrade module
    import pyetrade

    # Obtained secrets from Etrade for Sandbox or Live
    consumer_key = "<CONSUMER_KEY>"
    consumer_secret = "<SECRET_KEY>"

    tokens = {'oauth_token': '<TOKEN FROM THE SCRIPT ABOVE>',
              'oauth_token_secret': '<TOKEN FROM THE SCRIPT ABOVE>'}

    # Setting up the object used for alerts activity
    # Arg dev determines the environment Sandbox (dev=True)
    # or Live/Production (dev=False)

    orders = pyetrade.ETradeOrder(
        consumer_key,
        consumer_secret,
        tokens['oauth_token'],
        tokens['oauth_token_secret'],
        dev=True
    )

    # The above produces a json with all the accounts and their
    # respective accountIDKeys

    accountIDKey = '<Key for the chosen account from pyetrade.ETradeAccounts.list_accounts>'

    # Lists orders of a account
    print(orders.list_orders(accountIDKey, resp_format='json'))

    # place option order:
    action = "BUY_OPEN"
    symbol = "PLTR"
    callPut = "PUT"
    expiryDate = "2022-02-18"
    strikePrice = 23
    quantity = 1
    limitPrice=1.97
    orderTerm = "GOOD_UNTIL_CANCEL"  # "IMMEDIATE_OR_CANCEL"  # "GOOD_FOR_DAY"
    marketSession = "REGULAR"
    priceType = "LIMIT"
    clientOrderId = "ABC123456" # Unique alphanumeric identifier to prevent duplicate submissions of the same order

    resp = orders.place_option_order(
          resp_format="xml",
          accountIdKey = accountIDKey,
          symbol = symbol,
          callPut=callPut,
          expiryDate=expiryDate,
          strikePrice=strikePrice,
          orderAction=action,
          clientOrderId=clientOrderId,
          priceType= priceType,
          limitPrice=limitPrice,
          allOrNone=False,
          quantity=quantity,
          orderTerm=orderTerm,
          marketSession=marketSession,
        )
