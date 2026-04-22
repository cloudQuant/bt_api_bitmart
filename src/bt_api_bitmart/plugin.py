from __future__ import annotations

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_bitmart.exchange_data import BitmartExchangeDataSpot
from bt_api_bitmart.feeds.live_bitmart.spot import BitmartRequestDataSpot


def get_plugin_info() -> PluginInfo:
    return PluginInfo(
        name="bitmart",
        display_name="BitMart",
        version="0.1.0",
        supported_asset_types=["SPOT"],
        feed_classes=[BitmartRequestDataSpot],
        exchange_data_classes=[BitmartExchangeDataSpot],
    )
