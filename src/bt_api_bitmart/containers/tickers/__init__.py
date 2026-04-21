from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BitmartTickerData(TickerData):
    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "BITMART"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, dict) else None
        )
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.volume: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.ticker_data, dict):
            data = self.ticker_data
            self.ticker_symbol_name = from_dict_get_string(data, "symbol", self.symbol_name)
            self.last_price = from_dict_get_float(data, "last_price", 0.0)
            self.bid_price = from_dict_get_float(data, "bid_price", 0.0)
            self.ask_price = from_dict_get_float(data, "ask_price", 0.0)
            self.high = from_dict_get_float(data, "high_24h", 0.0)
            self.low = from_dict_get_float(data, "low_24h", 0.0)
            self.volume = from_dict_get_float(data, "volume_24h", 0.0)

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_last_price(self) -> float | None:
        self.init_data()
        return self.last_price

    def get_bid_price(self) -> float | None:
        self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        self.init_data()
        return self.ask_price

    def get_high(self) -> float | None:
        self.init_data()
        return self.high

    def get_low(self) -> float | None:
        self.init_data()
        return self.low

    def get_volume(self) -> float | None:
        self.init_data()
        return self.volume


class BitmartRequestTickerData(BitmartTickerData):
    pass


class BitmartWssTickerData(BitmartTickerData):
    pass
