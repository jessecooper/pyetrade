"""Alerts
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
    """ETradeAccounts:"""

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
    ):
        """__init_()
           """
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
        """list_alerts(dev, resp_format) -> resp
           param: resp_format
           description: Response format
           """
        api_url = "%s%s" % (self.base_url, ".json" if resp_format == "json" else "",)

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def list_alert_details(self, alert_id, resp_format="xml") -> dict:
        """list_alert_details(alert_id, dev, resp_format) -> resp
           param: alert_id
           type: int
           description: Numaric alert ID
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

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
        """delete_alert(alert_id, dev, resp_format) -> resp
           param: alert_id
           type: int
           description: Numaric alert ID
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format
           rformat: json
           rtype: dict
           rformat: other than json
           rtype: str"""

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
