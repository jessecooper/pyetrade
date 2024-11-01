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
        client_key: str,
        client_secret: str,
        resource_owner_key: str,
        resource_owner_secret: str,
        dev: bool = True,
    ):
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.base_url = f'https://{"apisb" if dev else "api"}.etrade.com/v1/user/alerts'
        self.session = OAuth1Session(
            self.client_key,
            self.client_secret,
            self.resource_owner_key,
            self.resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_alerts(
        self, count: int = 25, sort_order: str = "DESC", resp_format: str = "xml"
    ) -> dict:
        """:description: Lists alerts in Etrade

        :param count: The alert count, defaults to 25 (max 300)
        :type  count: int, optional
        :param sort_order: Sorting is done based on the createDate (ASC or DESC), defaults to DESC
        :type  sort_order: str, optional
        :param resp_format: Desired Response format, defaults to xml
        :type  resp_format: str, optional
        :return: List of alerts
        :rtype: ``xml`` or ``json`` based on ``resp_format``
        :EtradeRef: https://apisb.etrade.com/docs/api/user/api-alert-v1.html
        """

        api_url = "%s%s" % (
            self.base_url,
            ".json" if resp_format == "json" else "",
        )
        LOGGER.debug(api_url)

        if count >= 301:
            LOGGER.debug(
                f"Count {count} is greater than the max allowable value (300), using 300"
            )
            count = 300

        req = self.session.get(
            api_url, params={"count": count, "direction": sort_order}
        )

        req.raise_for_status()
        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def list_alert_details(
        self, alert_id: int, html_tags: bool = False, resp_format: str = "xml"
    ) -> dict:
        """:description: Provides details for an alert

        :param alert_id: Alert ID obtained from :class:`list_alerts`
        :type alert_id: int, required
        :param html_tags: The HTML tags on the alert, defaults to false. If set to true,
                          it returns the alert details msgText with html tags.
        :type  html_tags: bool, optional
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

        req = self.session.get(api_url, params={"htmlTags": html_tags})
        req.raise_for_status()

        LOGGER.debug(req.text)

        return xmltodict.parse(req.text) if resp_format.lower() == "xml" else req.json()

    def delete_alert(self, alert_id: int, resp_format: str = "xml") -> dict:
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
