from __future__ import annotations

from bt_api_base.registry import ExchangeRegistry

from bt_api_bitmart.plugin import get_plugin_info


def register():
    registry = ExchangeRegistry.get_instance()
    plugin_info = get_plugin_info()
    registry.register_plugin(plugin_info)
    return plugin_info
