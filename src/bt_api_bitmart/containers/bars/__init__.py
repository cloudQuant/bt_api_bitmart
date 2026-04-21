from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.bars.bar import BarData
from bt_api_base.functions.utils import from_dict_get_float


class BitmartBarData(BarData):
    def __init__(
        self,
        bar_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "BITMART"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.bar_data: dict[str, Any] | None = (
            bar_info if has_been_json_encoded and isinstance(bar_info, dict) else None
        )
        self.open_time: int | None = None
        self.open_price: float | None = None
        self.high_price: float | None = None
        self.low_price: float | None = None
        self.close_price: float | None = None
        self.volume: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.bar_data = json.loads(self.bar_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.bar_data, dict):
            data = self.bar_data
            self.open_time = int(from_dict_get_float(data, "timestamp") or 0)
            self.open_price = from_dict_get_float(data, "open")
            self.high_price = from_dict_get_float(data, "high")
            self.low_price = from_dict_get_float(data, "low")
            self.close_price = from_dict_get_float(data, "close")
            self.volume = from_dict_get_float(data, "volume")

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_open_time(self) -> int | None:
        self.init_data()
        return self.open_time

    def get_open_price(self) -> float | None:
        self.init_data()
        return self.open_price

    def get_high_price(self) -> float | None:
        self.init_data()
        return self.high_price

    def get_low_price(self) -> float | None:
        self.init_data()
        return self.low_price

    def get_close_price(self) -> float | None:
        self.init_data()
        return self.close_price

    def get_volume(self) -> float | None:
        self.init_data()
        return self.volume


class BitmartRequestBarData(BitmartBarData):
    pass


class BitmartWssBarData(BitmartBarData):
    pass
