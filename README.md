# pyetrade

Python E-Trade API Wrapper   
![alt text](https://img.shields.io/pypi/v/pyetrade.svg "PyPi Version Badge")
![alt text](https://img.shields.io/pypi/l/pyetrade.svg "PyPi License Badge")
![alt text](https://img.shields.io/pypi/pyversions/pyetrade.svg "PyPi Python Versions Badge")


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
