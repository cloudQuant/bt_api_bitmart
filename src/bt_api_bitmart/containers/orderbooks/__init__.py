"""Module-level docstring."""
from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_list


class BitmartOrderBookData(OrderBookData):
    """Class BitmartOrderBookData"""
    def __init__(
        self,
        orderbook_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """__init__ method"""
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BITMART"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.orderbook_data: dict[str, Any] | None = (
            orderbook_info if has_been_json_encoded and isinstance(orderbook_info, dict) else None
        )
        self.bids: list[list[float]] | None = None
        self.asks: list[list[float]] | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        """init_data method"""
        if not self.has_been_json_encoded:
            self.orderbook_data = json.loads(self.orderbook_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.orderbook_data, dict):
            data = self.orderbook_data
            bid_list = from_dict_get_list(data, "bids", [])
            ask_list = from_dict_get_list(data, "asks", [])
            self.bids = [
                [
                    from_dict_get_float(item, "price") or 0.0,
                    from_dict_get_float(item, "amount") or 0.0,
                ]
                for item in bid_list
            ]
            self.asks = [
                [
                    from_dict_get_float(item, "price") or 0.0,
                    from_dict_get_float(item, "amount") or 0.0,
                ]
                for item in ask_list
            ]

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        """get_exchange_name method"""
        return self.exchange_name

    def get_symbol_name(self) -> str:
        """get_symbol_name method"""
        return self.symbol_name

    def get_asset_type(self) -> str:
        """get_asset_type method"""
        return self.asset_type

    def get_bids(self) -> list[list[float]] | None:
        """get_bids method"""
        self.init_data()
        return self.bids

    def get_asks(self) -> list[list[float]] | None:
        """get_asks method"""
        self.init_data()
        return self.asks

    def get_local_update_time(self) -> float:
        """get_local_update_time method"""
        return float(self.local_update_time)


class BitmartRequestOrderBookData(BitmartOrderBookData):
    """Class BitmartRequestOrderBookData"""
    pass


class BitmartWssOrderBookData(BitmartOrderBookData):
    """Class BitmartWssOrderBookData"""
    pass
