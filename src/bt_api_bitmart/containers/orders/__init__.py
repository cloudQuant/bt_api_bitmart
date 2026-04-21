from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.orders.order import OrderData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BitmartOrderData(OrderData):
    def __init__(
        self,
        order_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(order_info, has_been_json_encoded)
        self.exchange_name = "BITMART"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.order_data: dict[str, Any] | None = (
            order_info if has_been_json_encoded and isinstance(order_info, dict) else None
        )
        self.order_id: str | None = None
        self.side: str | None = None
        self.order_type: str | None = None
        self.price: float | None = None
        self.amount: float | None = None
        self.status: str | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.order_data = json.loads(self.order_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.order_data, dict):
            data = self.order_data
            self.order_id = from_dict_get_string(data, "order_id")
            self.side = from_dict_get_string(data, "side")
            self.order_type = from_dict_get_string(data, "type")
            self.price = from_dict_get_float(data, "price")
            self.amount = from_dict_get_float(data, "size")
            self.status = from_dict_get_string(data, "status")

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_order_id(self) -> str | None:
        return self.order_id

    def get_side(self) -> str | None:
        return self.side

    def get_order_type(self) -> str | None:
        return self.order_type

    def get_price(self) -> float | None:
        return self.price

    def get_amount(self) -> float | None:
        return self.amount

    def get_status(self) -> str | None:
        return self.status


class BitmartRequestOrderData(BitmartOrderData):
    pass


class BitmartWssOrderData(BitmartOrderData):
    pass
