# pyetrade

Python E-Trade API Wrapper

## Install
```
git clone https://git.aigalactic.com/spyglass/pyetrade.git
cd pyetrade
sudo make init
sudo make install
```
## Example Usage
```
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
```
## Contribute to pyetrade
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
