#!/usr/bin/python3

"""Alerts
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
        self.base_url = r"https://%s.etrade.com/v1/user" % suffix
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

        if dev:
            uri = r"accounts/sandbox/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s.%s" % (self.base_url_dev, uri, resp_format)
            elif resp_format == "xml":
                api_url = "%s/%s" % (self.base_url_dev, uri)

        else:
            uri = r"accounts/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s.%s" % (self.base_url_prod, uri, resp_format)
            elif resp_format == "xml":
                api_url = "%s/%s" % (self.base_url_prod, uri)

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def read_alert(self, alert_id, dev=True, resp_format="json"):
        """read_alert(alert_id, dev, resp_format) -> resp
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

        if dev:
            uri = r"accounts/sandbox/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_dev,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_dev, uri, alert_id)

        else:
            uri = r"accounts/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_prod,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_prod, uri, alert_id)

        LOGGER.debug(api_url)
        req = self.session.get(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return req.text

    def delete_alert(self, alert_id, dev=True, resp_format="json"):
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

        if dev:
            uri = r"accounts/sandbox/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_dev,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_dev, uri, alert_id)

        else:
            uri = r"accounts/rest/alerts"
            if resp_format == "json":
                api_url = "%s/%s/%s.%s" % (
                    self.base_url_prod,
                    uri,
                    alert_id,
                    resp_format,
                )
            elif resp_format == "xml":
                api_url = "%s/%s/%s" % (self.base_url_prod, uri, alert_id)

        LOGGER.debug(api_url)
        req = self.session.delete(api_url)
        req.raise_for_status()
        LOGGER.debug(req.text)

        if resp_format == "json":
            return req.json()
        return req.text

   
