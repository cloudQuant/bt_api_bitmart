from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import urlencode

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed

from bt_api_bitmart.exchange_data import BitmartExchangeDataSpot


class BitmartRequestData(Feed):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self._api_key = kwargs.get("public_key") or kwargs.get("api_key") or ""
        self._api_secret = kwargs.get("private_key") or kwargs.get("api_secret") or ""
        self._api_memo = kwargs.get("memo") or kwargs.get("api_memo") or ""
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.exchange_name = kwargs.get("exchange_name", "BITMART___SPOT")
        self._params = BitmartExchangeDataSpot()
        self.request_logger = self.logger
        self.async_logger = self.logger

    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_DEALS,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.QUERY_ORDER,
            Capability.QUERY_OPEN_ORDERS,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_SERVER_TIME,
        }

    def _generate_signature(self, timestamp: Any, body_str: Any = "") -> str:
        if not self._api_secret:
            return ""
        message = f"{timestamp}#{self._api_memo}#{body_str}"
        return hmac.new(
            self._api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _unwrap(self, input_data: Any) -> Any:
        if isinstance(input_data, dict) and "data" in input_data:
            return input_data["data"]
        return input_data

    @staticmethod
    def _is_error(input_data: Any) -> bool:
        if not input_data:
            return True
        if isinstance(input_data, dict):
            code = input_data.get("code")
            if code is not None and code != 1000:
                return True
        return False

    def request(
        self,
        path: Any,
        params: dict[str, Any] | None = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: Any = 10,
        is_sign: Any = False,
    ) -> RequestData:
        if params is None:
            params = {}
        method, endpoint = path.split(" ", 1)
        timestamp = str(int(time.time() * 1000))
        headers = {"Content-Type": "application/json"}

        if is_sign and self._api_key:
            if method == "POST":
                body_str = json.dumps(body) if body else ""
            else:
                body_str = urlencode(sorted(params.items())) if params else ""
            headers["X-BM-KEY"] = self._api_key
            headers["X-BM-TIMESTAMP"] = timestamp
            headers["X-BM-SIGN"] = self._generate_signature(timestamp, body_str)

        if method == "GET":
            query_string = urlencode(params) if params else ""
            url = f"{self._params.rest_url}{endpoint}"
            if query_string:
                url = f"{url}?{query_string}"
            json_body = None
        else:
            url = f"{self._params.rest_url}{endpoint}"
            json_body = body

        res = self.http_request(method, url, headers, json_body, timeout)
        return RequestData(res, extra_data)

    async def async_request(
        self,
        path: Any,
        params: dict[str, Any] | None = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: Any = 5,
        is_sign: Any = False,
    ) -> RequestData:
        if params is None:
            params = {}
        method, endpoint = path.split(" ", 1)
        timestamp = str(int(time.time() * 1000))
        headers = {"Content-Type": "application/json"}

        if is_sign and self._api_key:
            if method == "POST":
                body_str = json.dumps(body) if body else ""
            else:
                body_str = urlencode(sorted(params.items())) if params else ""
            headers["X-BM-KEY"] = self._api_key
            headers["X-BM-TIMESTAMP"] = timestamp
            headers["X-BM-SIGN"] = self._generate_signature(timestamp, body_str)

        if method == "GET":
            query_string = urlencode(params) if params else ""
            url = f"{self._params.rest_url}{endpoint}"
            if query_string:
                url = f"{url}?{query_string}"
            json_body = None
        else:
            url = f"{self._params.rest_url}{endpoint}"
            json_body = body

        res = await self.async_http_request(method, url, headers, json_body, timeout)
        return RequestData(res, extra_data)

    def _get_server_time(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_server_time")
        params = {}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_server_time",
            symbol_name=None,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_server_time_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_server_time_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        return [{"server_time": data}], True

    def _get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_exchange_info")
        params = {}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_exchange_info",
            symbol_name=None,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_exchange_info_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if isinstance(data, dict):
            currencies = data.get("currencies", data)
            return [{"currencies": currencies}], True
        return [{"currencies": data}], True

    def _get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        bm_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_tick")
        params = {"symbol": bm_symbol}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_tick",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_tick_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_tick_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if not data:
            return [], False
        return [data], True

    def _get_depth(self, symbol: Any, count: Any = 35, extra_data: Any = None, **kwargs: Any):
        bm_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_depth")
        params = {"symbol": bm_symbol, "limit": min(count, 50)}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_depth",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_depth_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if not data:
            return [], False
        return [data], True

    def _get_kline(
        self,
        symbol: Any,
        period: Any = "1h",
        count: Any = 100,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        bm_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_kline")
        bm_step = self._params.get_period(period)
        params = {"symbol": bm_symbol, "step": bm_step, "limit": count}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_kline",
            symbol_name=symbol,
            period=period,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_kline_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if isinstance(data, dict):
            klines = data.get("klines", [])
            if klines:
                return klines, True
            return [], False
        if isinstance(data, list) and len(data) > 0:
            return data, True
        return [], False

    def _get_trade_history(
        self,
        symbol: Any,
        count: Any = 50,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        bm_symbol = self._params.get_symbol(symbol)
        path = self._params.get_rest_path("get_trades")
        params = {"symbol": bm_symbol, "limit": min(count, 50)}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_trades",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_trade_history_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_trade_history_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if isinstance(data, dict):
            trades = data.get("trades", [])
            return trades, len(trades) > 0
        if isinstance(data, list) and len(data) > 0:
            return data, True
        return [], False

    def _make_order(
        self,
        symbol: Any,
        size: Any,
        price: Any = None,
        order_type: Any = "buy-limit",
        extra_data: Any = None,
        **kwargs: Any,
    ):
        path = self._params.get_rest_path("make_order")
        bm_symbol = self._params.get_symbol(symbol)
        parts = order_type.lower().replace("-", " ").split()
        side = parts[0] if parts else "buy"
        otype = parts[1] if len(parts) > 1 else "limit"
        body = {"symbol": bm_symbol, "side": side, "type": otype, "size": str(size)}
        if price is not None and otype == "limit":
            body["price"] = str(price)
        if kwargs.get("notional"):
            body["notional"] = str(kwargs["notional"])
        if kwargs.get("client_order_id"):
            body["client_order_id"] = kwargs["client_order_id"]
        extra_data = self._update_extra_data(
            extra_data,
            request_type="make_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._make_order_normalize_function,
        )
        return path, body, extra_data

    @staticmethod
    def _make_order_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if not data:
            return [], False
        return [data], True

    def _cancel_order(
        self,
        symbol: Any = None,
        order_id: Any = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        path = self._params.get_rest_path("cancel_order")
        body = {}
        if symbol:
            body["symbol"] = self._params.get_symbol(symbol)
        if order_id:
            body["order_id"] = str(order_id)
        if kwargs.get("client_order_id"):
            body["client_order_id"] = kwargs["client_order_id"]
        extra_data = self._update_extra_data(
            extra_data,
            request_type="cancel_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._cancel_order_normalize_function,
        )
        return path, body, extra_data

    @staticmethod
    def _cancel_order_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        return [{"success": True}], True

    def _query_order(
        self,
        symbol: Any = None,
        order_id: Any = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        path = self._params.get_rest_path("query_order")
        body = {}
        if symbol:
            body["symbol"] = self._params.get_symbol(symbol)
        if order_id:
            body["orderId"] = str(order_id)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="query_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._query_order_normalize_function,
        )
        return path, body, extra_data

    @staticmethod
    def _query_order_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if not data:
            return [], False
        return [data], True

    def _get_open_orders(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_open_orders")
        body = {}
        if symbol:
            body["symbol"] = self._params.get_symbol(symbol)
        body["limit"] = kwargs.get("limit", 50)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_open_orders",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_open_orders_normalize_function,
        )
        return path, body, extra_data

    @staticmethod
    def _get_open_orders_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if isinstance(data, dict):
            orders = data.get("orders", [])
            return orders, True
        if isinstance(data, list):
            return data, True
        return [], False

    def _get_deals(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_deals")
        body = {}
        if symbol:
            body["symbol"] = self._params.get_symbol(symbol)
        body["limit"] = kwargs.get("limit", 50)
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_deals",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_deals_normalize_function,
        )
        return path, body, extra_data

    @staticmethod
    def _get_deals_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if isinstance(data, dict):
            orders = data.get("orders", [])
            return orders, True
        if isinstance(data, list):
            return data, True
        return [], False

    def _get_account(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_account")
        params = {}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_account",
            symbol_name=None,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_account_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if isinstance(data, dict):
            wallet = data.get("wallet", data)
            if isinstance(wallet, list):
                return wallet, True
            return [wallet], True
        return [data], True

    def _get_balance(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_balance")
        params = {}
        extra_data = self._update_extra_data(
            extra_data,
            request_type="get_balance",
            symbol_name=None,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=self._get_balance_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _get_balance_normalize_function(input_data: Any, extra_data: Any):
        if BitmartRequestData._is_error(input_data):
            return [], False
        data = BitmartRequestData._unwrap(input_data)
        if isinstance(data, dict):
            wallet = data.get("wallet", data)
            if isinstance(wallet, list):
                return wallet, True
            return [wallet], True
        if isinstance(data, list):
            return data, True
        return [data], True

    def _update_extra_data(self, extra_data, **kwargs):
        if extra_data is None:
            extra_data = {}
        extra_data.update(kwargs)
        return extra_data
