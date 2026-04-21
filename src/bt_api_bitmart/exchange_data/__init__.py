from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BitmartExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITMART___SPOT"
        self.asset_type = "SPOT"
        self.rest_url = "https://api-cloud.bitmart.com"
        self.wss_url = "wss://ws-manager-compress.bitmart.com/api?protocol=1.1"
        self.rest_paths = {}
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1",
            "3m": "3",
            "5m": "5",
            "15m": "15",
            "30m": "30",
            "45m": "45",
            "1h": "60",
            "2h": "120",
            "3h": "180",
            "4h": "240",
            "1d": "1440",
            "1w": "10080",
            "1M": "43200",
        }
        self.legal_currency = ["USDT", "USD", "BTC", "ETH", "USDC"]

    def get_symbol(self, symbol: str) -> str:
        return symbol.upper().replace("/", "_").replace("-", "_")

    def get_period(self, period: str) -> str:
        return self.kline_periods.get(period, period)

    def get_rest_path(self, request_type: str, **kwargs) -> str:
        path = self.rest_paths.get(request_type)
        if path is None:
            raise ValueError(f"[{self.exchange_name}] Unknown rest path: {request_type}")
        return str(path)

    def get_wss_path(self, channel_type, symbol: str | None = None, **kwargs) -> str:
        path = self.wss_paths.get(channel_type, "")
        if symbol and "{symbol}" in str(path):
            path = str(path).replace("{symbol}", self.get_symbol(symbol))
        return str(path)


class BitmartExchangeDataSpot(BitmartExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.exchange_name = "BITMART___SPOT"
        self.rest_url = "https://api-cloud.bitmart.com"
        self.wss_url = "wss://ws-manager-compress.bitmart.com/api?protocol=1.1"
        self.rest_paths = {
            "get_server_time": "GET /spot/v1/time",
            "get_exchange_info": "GET /spot/v1/currencies",
            "get_tick": "GET /spot/quotation/v3/ticker",
            "get_tick_all": "GET /spot/quotation/v3/tickers",
            "get_depth": "GET /spot/quotation/v3/books",
            "get_trades": "GET /spot/quotation/v3/trades",
            "get_kline": "GET /spot/quotation/v3/klines",
            "make_order": "POST /spot/v2/submit_order",
            "cancel_order": "POST /spot/v3/cancel_order",
            "cancel_all_orders": "POST /spot/v4/cancel_all",
            "query_order": "POST /spot/v4/query/order",
            "get_open_orders": "POST /spot/v4/query/open-orders",
            "get_deals": "POST /spot/v4/query/history-orders",
            "get_balance": "GET /spot/v1/wallet",
            "get_account": "GET /spot/v1/wallet",
        }


BitmartSpotExchangeData = BitmartExchangeDataSpot
