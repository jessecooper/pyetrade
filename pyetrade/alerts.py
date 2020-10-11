"""Alerts - ETrade Alerts API

   TODO:
    * list_alerts - add args
    * list_alert_details - add arg

"""

import logging
import xmltodict
from requests_oauthlib import OAuth1Session

# Set up logging
LOGGER = logging.getLogger(__name__)


class ETradeAlerts(object):
    """:description: Object to retrieve alerts

       :param client_key: Client key provided by Etrade
       :type client_key: str, required
       :param client_secret: Client secret provided by Etrade
       :type client_secret: str, required
       :param resource_owner_key: Resource key from :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_key: str, required
       :param resource_owner_secret: Resource secret from
              :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_secret: str, required
       :param dev: Defines Sandbox (True) or Live (False) ETrade, defaults to True
       :type dev: bool, optional
       :EtradeRef: https://apisb.etrade.com/docs/api/user/api-alert-v1.html

    """

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
    ):
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        suffix = "apisb" if dev else "api"
        self.base_url = r"https://%s.etrade.com/v1/user/alerts" % suffix
        self.session = OAuth1Session(
            self.client_key,
            self.client_secret,
            self.resource_owner_key,
            self.resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_alerts(self, resp_format="xml") -> dict:
        """:description: Lists alerts in Etrade

           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: List of alerts
           :rtype: ``xml`` or ``json`` based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/user/api-alert-v1.html

           """
        api_url = "%s%s" % (self.base_url, ".json" if resp_format == "json" else "",)

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def list_alert_details(self, alert_id, resp_format="xml") -> dict:
        """:description: Provides details for an alert

           :param alert_id: Alert ID obtained from :class:`list_alerts`
           :type alert_id: int, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: List of alert details
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/user/api-alert-v1.html

           """

        api_url = "%s%s/%s" % (
            self.base_url,
            ".json" if resp_format == "json" else "",
            alert_id,
        )

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def delete_alert(self, alert_id, resp_format="xml"):
        """:description: Deletes specified alert

           :param alert_id: Alert ID obtained from :class:`list_alerts`
           :type alert_id: int, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :return: List of alert details
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/user/api-alert-v1.html

        """

        api_url = "%s%s/%s" % (
            self.base_url,
            ".json" if resp_format == "json" else "",
            alert_id,
        )

        LOGGER.debug(api_url)
        req = self.session.delete(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()
