# pyetrade

Python E-Trade API Wrapper

## Install
	git clone https://git.aigalactic.com/spyglass/pyetrade.git
	cd pyetrade
	sudo make init
	sudo make install

## Usage
	from pyetrade import ETradeAPI
	etrade = ETradeAPI(consumer_key, consumer_secret)
	etrade.get_request_token()
	#Follow url and get verification code
	etrade.get_access_token(verifier_code)
