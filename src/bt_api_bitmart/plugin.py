"""Module-level docstring."""
from __future__ import annotations

from typing import Any

from bt_api_base.plugins.protocol import PluginInfo
from bt_api_bitmart import __version__
from bt_api_bitmart.exchange_data import BitmartExchangeDataSpot
from bt_api_bitmart.feeds.live_bitmart.spot import BitmartRequestDataSpot


def get_plugin_info() -> PluginInfo:
    """get_plugin_info function"""
    return PluginInfo(
        name="bt_api_bitmart",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("BITMART___SPOT",),
        supported_asset_types=("SPOT",),
    )


def register_plugin(registry: Any, runtime_factory: Any) -> PluginInfo:
    """register_plugin function"""
    registry.register_feed("BITMART___SPOT", BitmartRequestDataSpot)
    registry.register_exchange_data("BITMART___SPOT", BitmartExchangeDataSpot)
    return get_plugin_info()
