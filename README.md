# pyetrade

Python E-Trade API Wrapper

## Install
	git clone https://git.aigalactic.com/spyglass/pyetrade.git
	cd pyetrade
	sudo make init
	sudo make install

## Usage
	import pyetrade
	oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
	oauth.get_request_token()
	#Follow url and get verification code
	tokens = oauth.get_access_token(verifier_code)
	accounts = pyetrade.ETradeAccounts(consumer_key,
					   consumer_secret, 
					   tokens['oauth_token'],
				           tokens['oauth_token_secret'])
	accounts.list_accounts()

## Contribute too pyetrade
Please read contribution wiki for development guide https://git.aigalactic.com/Spyglass/pyetrade/wiki/Contributing-to-PyEtrade
