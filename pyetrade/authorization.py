"""Authorization - ETrade Authorization API Calls

   TODO:
    * Lint this messy code
    * Catch events

    """

import logging
from requests_oauthlib import OAuth1Session

# Set up logging
LOGGER = logging.getLogger(__name__)


class ETradeOAuth(object):
    """:description: Performs authorization for OAuth 1.0a

       :param client_key: Client key provided by Etrade
       :type client_key: str, required
       :param client_secret: Client secret provided by Etrade
       :type client_secret: str, required
       :param callback_url: Callback URL passed to OAuth mod, defaults to "oob"
       :type callback_url: str, optional
       :EtradeRef: https://apisb.etrade.com/docs/api/authorization/request_token.html

    """

    def __init__(self, consumer_key, consumer_secret, callback_url="oob"):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url_prod = r"https://api.etrade.com"
        self.base_url_dev = r"https://apisb.etrade.com"
        self.req_token_url = r"https://api.etrade.com/oauth/request_token"
        self.auth_token_url = r"https://us.etrade.com/e/t/etws/authorize"
        self.access_token_url = r"https://api.etrade.com/oauth/access_token"
        self.callback_url = callback_url
        self.access_token = None
        self.resource_owner_key = None

    def get_request_token(self):
        """:description: Obtains the token URL from Etrade.

           :param None: Takes no parameters
           :return: Formatted Authorization URL (Access this to obtain taken)
           :rtype: str
           :EtradeRef: https://apisb.etrade.com/docs/api/authorization/request_token.html

        """

        # Set up session
        self.session = OAuth1Session(
            self.consumer_key,
            self.consumer_secret,
            callback_uri=self.callback_url,
            signature_type="AUTH_HEADER",
        )
        # get request token
        self.session.fetch_request_token(self.req_token_url)
        # get authorization url
        # etrade format: url?key&token
        authorization_url = self.session.authorization_url(self.auth_token_url)
        akey = self.session.parse_authorization_response(authorization_url)
        # store oauth_token
        self.resource_owner_key = akey["oauth_token"]
        formated_auth_url = "%s?key=%s&token=%s" % (
            self.auth_token_url,
            self.consumer_key,
            akey["oauth_token"],
        )
        self.verifier_url = formated_auth_url
        LOGGER.debug(formated_auth_url)

        return formated_auth_url

    def get_access_token(self, verifier):
        """:description: Obtains access token. Requires token URL from :class:`get_request_token`

           :param verifier: OAuth Verification Code from Etrade
           :type verifier: str, required
           :return: OAuth access tokens
           :rtype: dict
           :EtradeRef: https://apisb.etrade.com/docs/api/authorization/get_access_token.html

        """

        # Set verifier
        self.session._client.client.verifier = verifier
        # Get access token
        self.access_token = self.session.fetch_access_token(self.access_token_url)
        LOGGER.debug(self.access_token)

        return self.access_token


class ETradeAccessManager(object):
    """:description: Renews and revokes ETrade OAuth access tokens

       :param client_key: Client key provided by Etrade
       :type client_key: str, required
       :param client_secret: Client secret provided by Etrade
       :type client_secret: str, required
       :param resource_owner_key: Resource key from :class:`ETradeOAuth`
       :type resource_owner_key: str, required
       :param resource_owner_secret: Resource secret from :class:`ETradeOAuth`
       :type resource_owner_secret: str, required
       :EtradeRef: https://apisb.etrade.com/docs/api/authorization/renew_access_token.html

    """

    def __init__(
        self, client_key, client_secret, resource_owner_key, resource_owner_secret
    ):
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.renew_access_token_url = r"https://api.etrade.com/oauth/renew_access_token"
        self.revoke_access_token_url = (
            r"https://api.etrade.com/oauth/revoke_access_token"
        )
        self.session = OAuth1Session(
            self.client_key,
            self.client_secret,
            self.resource_owner_key,
            self.resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def renew_access_token(self):
        """:description: Renews access tokens obtained from :class:`ETradeOAuth`

           :param None: Takes no parameters
           :return: Success or failure
           :rtype: bool (True or False)
           :EtradeRef: https://apisb.etrade.com/docs/api/authorization/renew_access_token.html

        """
        resp = self.session.get(self.renew_access_token_url)
        LOGGER.debug(resp.text)
        resp.raise_for_status()

        return True

    def revoke_access_token(self):
        """:description: Revokes access tokens obtained from :class:`ETradeOAuth`

           :param None: Takes no parameters
           :return: Success or failure
           :rtype: bool (True or False)
           :EtradeRef: https://apisb.etrade.com/docs/api/authorization/revoke_access_token.html

        """
        resp = self.session.get(self.revoke_access_token_url)
        LOGGER.debug(resp.text)
        resp.raise_for_status()

        return True
