#!/usr/bin/python3

"""Order - ETrade Order API
   TODO:
       * Preview equity order change
       * Place equity order change
       * Preview option order
       * Place option order
       * Preview option order change
       * Place option order change
"""

import logging
import jxmlease
from requests_oauthlib import OAuth1Session

LOGGER = logging.getLogger(__name__)


class OrderException(Exception):
    """
    Exception raised when giving bad args to a method
    not from Etrade calls
    """

    def __init__(self, explanation=None, params=None):
        super().__init__()
        self.required = params
        self.args = (explanation, params)

    def __str__(self):
        return "Missing required parameters"


class ETradeOrder:
    """ETradeOrder"""

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
        timeout=30,
    ):
        """__init__(client_key, client_secret, resource_owner_key, resource_owner_secret, dev=True)

           param: client_key
           type: str
           description: etrade client key

           param: client_secret
           type: str
           description: etrade client secret

           param: resource_owner_key
           type: str
           description: OAuth authentication token key

           param: resource_owner_secret
           type: str
           description: OAuth authentication token secret

           param: dev
           type: boolean
           description: use the development environment (True) or production (False)

           param: timeout
           type: int
           description: request timeout, default 30s

        """
        self.base_url = (
            r"https://apisb.etrade.com/v1/accounts"
            if dev
            else r"https://api.etrade.com/v1/accounts"
        )
        self.dev_environment = dev
        self.timeout = timeout
        self.session = OAuth1Session(
            client_key,
            client_secret,
            resource_owner_key,
            resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_orders(self, account_id, resp_format="json", **kwargs):
        """ list_orders(dev, resp_format='json', **kwargs) -> resp

            param: account_id
            type: string
            required: true
            description: account ID Key

            description: see ETrade API docs

        """
        assert resp_format in ("json", "xml")
        api_url = self.base_url + "/" + account_id + "/orders"
        if resp_format == "json":
            api_url += ".json"

        # Build Params
        params = kwargs
        LOGGER.debug("query string params: %s", params)

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=params, timeout=self.timeout)
        LOGGER.debug(req.text)
        req.raise_for_status()

        if resp_format == "json":
            return req.json()
        return req.text

    def check_order(self, **kwargs):
        """
        check that required params
        for preview or place order are there
        and correct
        """
        mandatory = [
            "accountId",
            "symbol",
            "orderAction",
            "clientOrderId",
            "priceType",
            "quantity",
            "orderTerm",
            "marketSession",
        ]
        if not all(param in kwargs for param in mandatory):
            raise OrderException

        if kwargs["priceType"] == "STOP" and "stopPrice" not in kwargs:
            raise OrderException
        if kwargs["priceType"] == "LIMIT" and "limitPrice" not in kwargs:
            raise OrderException
        if (
            kwargs["priceType"] == "STOP_LIMIT"
            and "limitPrice" not in kwargs
            and "stopPrice" not in kwargs
        ):
            raise OrderException

    def build_order_payload(self, order_type, **kwargs):
        """
        build the POST payload of a preview or place order

            param: order_type
            type: string
            required: true
            description: PreviewOrderRequest or PlaceOrderRequest
        """
        instrument = {
            "Product": {"securityType": "EQ", "symbol": kwargs["symbol"]},
            "orderAction": kwargs["orderAction"],
            "quantityType": "QUANTITY",
            "quantity": kwargs["quantity"],
        }
        order = kwargs
        order["Instrument"] = instrument
        order["stopPrice"] = ""
        payload = {
            order_type: {
                "orderType": "EQ",
                "clientOrderId": kwargs["clientOrderId"],
                "Order": order,
            }
        }

        if "previewId" in kwargs:
            payload[order_type]["PreviewIds"] = {"previewId": kwargs["previewId"]}

        return payload

    def perform_request(self, method, resp_format, api_url, payload):
        """
        run a post or put request
        with json or xml
        used by preview, place and cancel
        """

        LOGGER.debug(api_url)
        LOGGER.debug("payload: %s", payload)
        if resp_format == "json":
            req = method(api_url, json=payload, timeout=self.timeout)
        else:
            headers = {"Content-Type": "application/xml"}
            payload = jxmlease.emit_xml(payload)
            LOGGER.debug("xml payload: %s", payload)
            req = method(api_url, data=payload, headers=headers, timeout=self.timeout)

        LOGGER.debug(req.text)
        req.raise_for_status()

        if resp_format == "json":
            return req.json()
        if resp_format is None:
            return jxmlease.parse(req.text)
        return req.text

    def preview_equity_order(self, resp_format=None, **kwargs):
        """preview_equity_order(dev, resp_format, **kwargs) -> resp

           param: resp_format
           type: str
           description: Response format JSON or None = XML

           kwargs:
           param: accountId
           type: string
           required: true
           description: account ID Key

           param: symbol
           type: str
           required: true
           description: The market symbol for the security being bought or sold

           param: orderAction
           type: str
           required: true
           description: The action that the broker is requested
                        to perform Possible values are:
                            * BUY
                            * SELL
                            * BUY_TO_COVER
                            * SELL_SHORT

           param: previewId
           type: long
           required: conditional
           description: If the order was not previewed, this
                        parameter should not be specified. If
                        the order was previewed, this parameter
                        must specify the numeric preview ID from
                        the preview, and other parameters of
                        this request must match the parameters
                        of the preview

           param: clientOrderId
           type: str
           required: true
           description: A reference number generated by the
                        developer. Used to ensure that a
                        duplicate order is not being submitted.
                        It can be any value of 20 alphanmeric
                        characters or less, but must be unique
                        within this account. It does not appear
                        in any API responses.

           param: priceType
           type: str
           required: true
           description: The type of pricing specified in the
                        equity order. Possible values are:
                            * MARKET
                            * LIMIT
                            * STOP
                            * STOP_LIMIT
                            * MARKET_ON_CLOSE
                        If STOP, requires a stopPrice. If LIMIT,
                        requires a limitPrice. if STOP_LIMIT,
                        requires both. For more information
                        on these values, refer to the E-Trade
                        online help on conditional orders

           param: limitPrice
           type: double
           required: conditional
           description: The highest price at which to buy or
                        lowest price at which to sell. Required
                        if priceType is STOP or STOP_LIMIT.

           param: stopPrice
           type: double
           required: conditional
           description: The price at which to buy or sell if
                        specified in a stop order. Required if
                        priceType is STOP or STOP_LIMIT.

           param: allOrNone
           type: bool
           required: optional
           description: If TRUE, the transactions specified in
                        the order must be executed all at once
                        or not at all. Default is FALSE.

           param: quantity
           type: int
           required: true
           description: The number of shares to buy or sell

           param: reserveOrder
           type: bool
           required: optional
           description: If set to TRUE, publicly displays only
                        a limited number of shares (the
                        reserve quantity), instead of the
                        entire order, to avoid influencing
                        other traders. Default is FALSE. If
                        TRUE, must also specify the
                        reserveQuantity.

           param: reserveQuantity
           type: int
           required: conditional
           description: The number of shares to be publicly
                        displayed if this is a reserve order.
                        Required if serveOrder is True.

           param: marketSession
           type: str
           required: true
           description: Session in which the equity order will
                        be placed. Possible values are:
                            * REGULAR
                            * EXTENDED
           param: orderTerm
           type: str
           required: true
           description: Specifies the term for which the order
                        is in effect. Possible values are:
                            * GOOD_UNTIL_CANCEL
                            * GOOD_FOR_DAY
                            * IMMEDIATE_OR_CANCEL (only for
                              limit orders)
                            * FILL_OR_KILL (only for limit
                              orders)

           param: routingDestination
           type: str
           required: optional
           description: The exchange where the order should be
                        executed. Users may want to specify
                        this if they believe they can get a
                        better order fill at a specific exchange
                        rather than relying on automatic order
                        routing system. Posssible values are:
                            * AUTO (default)
                            * ARCA
                            * NSDQ
                            * NYSE

           param: accountId
           type: int
           description: Numeric account ID

           param: allOrNone
           type: bool

           description: if True, the transaction specified in
                         the order are to be executed all at
                         once, or not at all
           param: estimatedCommission
           type: double

           description: The cost billed to the user to preform
                         the requested action
           param: estimatedTotalAmount
           type: double

           description: The cost or proceeds, including broker
                         commission, resulting from the requested
                         action

           param: messageList
           type: dict
           description: Container for messages describing the
                         result of the action

           param: msgDesc
           type: str
           description: Text of the result message,
                            indicating order status, success or
                            failure, additional requirements
                            that must be met before placing the
                            order, etc. Applications typically
                            display this message to the user,
                            which may result in further user
                            action
            param: msgCode
            type: int
            description: Standard numeric code of the result
                            message. Refer to the Error Messages
                            documentation for examples. May
                            optionally be displayed to the user,
                            but is primarily intended for
                            internal use.

           param: orderNum
           type: int
           description: Numeric ID for this order in the E*TRADE
                         system

           param: orderTime
           type: long
           description: The time the order was submitted, in
                         epoch time.
           param: symbolDesc
           type: str
           description: Text description of the security

           param: symbol
           type: str
           description: The market symbol for the underlier

           param: quantity
           type: int
           description: The number of shares to buy or sell

           param: reserveOrder
           type: bool
           description: If TRUE, this is a reserve order -
                         meaning that only a limited number
                         of shares will be publicly displayed,
                         instead of the entire order, to
                         avoid influencing other traders.

           param: orderTerm
           type: str
           description: Specifies the term for which the
                         order is in effect. Possible values
                         are:
                             * GOOD_UNTIL_CANCEL
                             * GOOD_FOR_DAY
                             * IMMEDIATE_OR_CANCEL (only for
                                limit orders)
                             * FILL_OR_KILL (only for limit
                                orders)
           param: orderAction
           type: str
           description: The action that the broker is requested
                         to perform. Possible values are:
                             * BUY
                             * SELL
                             * BUY_TO_COVER
                             * SELL_SHORT

            param: priceType
           type: str
           description: The type of pricing. Possible values are:
                            * MARKET
                            * LIMIT
                            * STOP
                            * STOP_LIMIT
                            * MARKET_ON_CLOSE

            param: limitPrice
           type: double
           description: The highest price at which to buy or the
                         lowest price at which to sell if specified
                         in a limit order. Returned if priceType is
                         LIMIT

            param: stopPrice
           type: double
           description: The price at which a stock is to be bought
                         or sold if specified in a stop order.
                         Returned if priceType is STOP.

            param: routingDestination
           type: str
           description: The exchange where the order should be
                         executed. Possible values are:
                             * AUTO
                             * ARCA
                             * NSDQ
                             * NYSE

        """
        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/preview"
        # payload creation
        payload = self.build_order_payload("PreviewOrderRequest", **kwargs)

        return self.perform_request(self.session.post, resp_format, api_url, payload)
   
    def change_preview_equity_order(self, resp_format=None, **kwargs):
        """
        Same as preview_equity_order() above, but with orderId 
        param: orderId
           type: str
           description: The orderId you want to modify
        """
        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/"+kwargs["orderId"]+"/change/preview"
        # payload creation
        payload = self.build_order_payload("PreviewOrderRequest", **kwargs)

        return self.perform_request(self.session.put, resp_format, api_url, payload)

    def place_equity_order(self, resp_format=None, **kwargs):
        """place_equity_order(dev, resp_format, **kwargs) -> resp

           param: resp_format
           type: str
           description: Response format JSON or None = XML

           kwargs: see preview_equity_order
        """

        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        if "previewId" not in kwargs:
            LOGGER.debug(
                "No previewId given, previewing before placing order "
                "because of an Etrade bug as of 1/1/2019"
            )
            preview = self.preview_equity_order(resp_format, **kwargs)
            if resp_format == "xml":
                preview = jxmlease.parse(preview)
            kwargs["previewId"] = preview["PreviewOrderResponse"]["PreviewIds"][
                "previewId"
            ]
            LOGGER.debug(
                "Got a successful preview with previewId: %s", kwargs["previewId"]
            )

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/place"
        # payload creation
        payload = self.build_order_payload("PlaceOrderRequest", **kwargs)

        return self.perform_request(self.session.post, resp_format, api_url, payload)
      
    def place_changed_equity_order(self, resp_format=None, **kwargs):
        """place_changed_equity_order(dev, resp_format, **kwargs) -> resp

           param: resp_format
           type: str
           description: Response format JSON or None = XML

           kwargs: see change_preview_equity_order
        """

        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        if "previewId" not in kwargs:
            LOGGER.debug(
                "No previewId given, previewing before placing order "
                "because of an Etrade bug as of 1/1/2019"
            )
            preview = self.preview_equity_order(resp_format, **kwargs)
            if resp_format == "xml":
                preview = jxmlease.parse(preview)
            kwargs["previewId"] = preview["PreviewOrderResponse"]["PreviewIds"][
                "previewId"
            ]
            LOGGER.debug(
                "Got a successful preview with previewId: %s", kwargs["previewId"]
            )

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/"+kwargs["orderId"]+"change/place"
        # payload creation
        payload = self.build_order_payload("PlaceOrderRequest", **kwargs)

        return self.perform_request(self.session.put, resp_format, api_url, payload)
      
    def cancel_order(self, account_id, order_num, resp_format=None):
        """ cancel_order(account_id, order_num, dev, resp_format)
            param: account_id
            type: string
            description: account id key

            param: order_num
            type: int
            description: numeric id for this order in the etrade system

            param: dev
            type: bool
            description: API enviornment

            param: resp_format
            type: str
            description: Response format JSON or None = XML

        """
        assert resp_format in (None, "json", "xml")
        api_url = self.base_url + "/" + account_id + "/orders/cancel"
        payload = {"CancelOrderRequest": {"orderId": order_num}}

        return self.perform_request(self.session.put, resp_format, api_url, payload)
