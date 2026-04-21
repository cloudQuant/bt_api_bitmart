# bt_api_bitmart

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitmart.svg)](https://pypi.org/project/bt_api_bitmart/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitmart.svg)](https://pypi.org/project/bt_api_bitmart/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitmart/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitmart/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitmart/badge/?version=latest)](https://bt-api-bitmart.readthedocs.io/)

---

<!-- English -->
# bt_api_bitmart

> **BitMart exchange plugin for bt_api** — Unified REST API for **Spot** trading with market data, trading operations, and account management.

`bt_api_bitmart` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **BitMart** exchange. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitmart.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitmart.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bitmart |
| PyPI | https://pypi.org/project/bt_api_bitmart/ |
| Issues | https://github.com/cloudQuant/bt_api_bitmart/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### 1 Asset Type

| Asset Type | Code | REST | Description |
|---|---|---|---|
| Spot | `BITMART___SPOT` | ✅ | Spot trading |

### REST API

- **Market Data** — Ticker, order book depth, k-lines, trade history
- **Trading** — Place orders, cancel orders, query order status, get open orders
- **Account** — Account info, balance queries

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
        "memo": "your_memo",
    }
})

ticker = api.get_tick("BITMART___SPOT", "BTCUSDT")
balance = api.get_balance("BITMART___SPOT")
order = api.make_order(exchange_name="BITMART___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### Unified Data Containers

All exchange responses normalized to bt_api_base container types:

- `TickContainer` — 24hr rolling ticker
- `OrderBookContainer` — Order book depth
- `BarContainer` — K-line/candlestick
- `TradeContainer` — Individual trades
- `OrderContainer` — Order status and fills
- `AccountBalanceContainer` — Asset balances

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bitmart
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bitmart
cd bt_api_bitmart
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `requests` for HTTP client
- `websocket-client` for WebSocket (future)
- `aiohttp` for async HTTP

---

## Quick Start

### 1. Install

```bash
pip install bt_api_bitmart
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BITMART___SPOT", "BTCUSDT")
print(f"BTCUSDT price: {ticker}")
```

### 3. Place an order (requires API key)

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
        "memo": "your_memo",
    }
})

order = api.make_order(
    exchange_name="BITMART___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"Order placed: {order}")
```

### 4. Query order status

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
        "memo": "your_memo",
    }
})

# Query specific order
order = api.query_order(exchange_name="BITMART___SPOT", order_id="your_order_id")
print(f"Order status: {order}")

# Get all open orders
open_orders = api.get_open_orders("BITMART___SPOT")
print(f"Open orders: {open_orders}")
```

### 5. Get account balance

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
        "memo": "your_memo",
    }
})

balance = api.get_balance("BITMART___SPOT")
print(f"Balance: {balance}")
```

---

## Architecture

```
bt_api_bitmart/
├── plugin.py                     # register_plugin() — bt_api plugin entry point
├── registry_registration.py        # register() — feeds / exchange_data registration
├── __init__.py                    # Package exports
├── exchange_data/
│   └── __init__.py              # BitmartExchangeData, BitmartExchangeDataSpot
├── feeds/
│   └── live_bitmart/
│       ├── __init__.py          # Module exports
│       ├── spot.py              # BitmartRequestDataSpot — all SPOT REST endpoints
│       └── request_base.py       # BitmartRequestData — base class with signature logic
├── containers/
│   ├── __init__.py
│   ├── orders/__init__.py
│   ├── balances/__init__.py
│   ├── accounts/__init__.py
│   ├── bars/__init__.py
│   ├── tickers/__init__.py
│   └── orderbooks/__init__.py
└── errors/
    └── __init__.py
```

---

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_ticker` / `get_tick` | 24hr rolling ticker |
| | `get_depth` | Order book depth (max 50 levels) |
| | `get_kline` / `get_bars` | K-line/candlestick (1m to 1M) |
| | `get_trades` / `get_trade_history` | Recent trade history |
| | `get_server_time` | Server time sync |
| | `get_exchange_info` | Exchange symbol info |
| **Account** | `get_balance` | Asset balances |
| | `get_account` | Full account info |
| **Trading** | `make_order` | Place limit/market orders |
| | `cancel_order` | Cancel single order |
| | `query_order` | Query order by ID |
| | `get_open_orders` | All open orders |
| | `get_deals` | Order deal history |

---

## BitMart API Details

### Base URLs

| Environment | REST API | WebSocket |
|---|---|---|
| Production | `https://api-cloud.bitmart.com` | `wss://ws-manager-compress.bitmart.com/api?protocol=1.1` |

### Authentication

BitMart API uses HMAC-SHA256 signature:

```
Message = timestamp#memo#body_str
Signature = HMAC-SHA256(api_secret, Message)
```

Required headers:
- `X-BM-KEY` — API key
- `X-BM-TIMESTAMP` — Timestamp in milliseconds
- `X-BM-SIGN` — HMAC-SHA256 signature

### Symbol Format

BitMart uses underscore format: `BTCUSDT`, `ETHUSDT`

### Supported Periods for K-lines

| Period | BitMart Code |
|---|---|
| 1m | 1 |
| 3m | 3 |
| 5m | 5 |
| 15m | 15 |
| 30m | 30 |
| 45m | 45 |
| 1h | 60 |
| 2h | 120 |
| 3h | 180 |
| 4h | 240 |
| 1d | 1440 |
| 1w | 10080 |
| 1M | 43200 |

---

## Error Handling

All BitMart API errors are translated to bt_api_base `ApiError` subclasses. Common error codes:

| Code | Description |
|---|---|
| 1000 | Success |
| 50000-59999 | API error |
| 50002 | Invalid signature |
| 50003 | Invalid API key |
| 50004 | Invalid timestamp |
| 50005 | Permission denied |
| 50006 | Too many requests |

---

## Rate Limits

| Endpoint Type | Limit |
|---|---|
| Public endpoints | 200 requests/10s |
| Private endpoints | 100 requests/10s |
| Order placement | 200 requests/10s |

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-bitmart.readthedocs.io/ |
| **中文** | https://bt-api-bitmart.readthedocs.io/zh/latest/ |
| API Reference | https://bt-api-bitmart.readthedocs.io/api/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bitmart/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 BitMart 交易所插件** — 为**现货**交易提供统一的 REST API，包括市场数据、交易操作和账户管理。

`bt_api_bitmart` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，连接 **BitMart** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitmart.readthedocs.io/ |
| 中文文档 | https://bt-api-bitmart.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bitmart |
| PyPI | https://pypi.org/project/bt_api_bitmart/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitmart/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 1 种资产类型

| 资产类型 | 代码 | REST | 说明 |
|---|---|---|---|
| 现货 | `BITMART___SPOT` | ✅ | 现货交易 |

### REST API

- **市场数据** — 行情、订单簿深度、K线、成交历史
- **交易** — 下单、撤单、查询订单状态、获取挂单
- **账户** — 账户信息、余额查询

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
        "memo": "your_memo",
    }
})

ticker = api.get_tick("BITMART___SPOT", "BTCUSDT")
balance = api.get_balance("BITMART___SPOT")
order = api.make_order(exchange_name="BITMART___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### 统一数据容器

所有交易所响应规范化为 bt_api_base 容器类型：

- `TickContainer` — 24小时滚动行情
- `OrderBookContainer` — 订单簿深度
- `BarContainer` — K线/蜡烛图
- `TradeContainer` — 逐笔成交
- `OrderContainer` — 订单状态和成交
- `AccountBalanceContainer` — 资产余额

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bitmart
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bitmart
cd bt_api_bitmart
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `requests` HTTP 客户端
- `websocket-client` WebSocket（未来）
- `aiohttp` 异步 HTTP

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_bitmart
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BITMART___SPOT", "BTCUSDT")
print(f"BTCUSDT 价格: {ticker}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
        "memo": "your_memo",
    }
})

order = api.make_order(
    exchange_name="BITMART___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"订单已下单: {order}")
```

### 4. 查询订单状态

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
        "memo": "your_memo",
    }
})

# 查询指定订单
order = api.query_order(exchange_name="BITMART___SPOT", order_id="your_order_id")
print(f"订单状态: {order}")

# 获取所有挂单
open_orders = api.get_open_orders("BITMART___SPOT")
print(f"挂单: {open_orders}")
```

### 5. 获取账户余额

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITMART___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
        "memo": "your_memo",
    }
})

balance = api.get_balance("BITMART___SPOT")
print(f"余额: {balance}")
```

---

## 架构

```
bt_api_bitmart/
├── plugin.py                     # register_plugin() — bt_api 插件入口
├── registry_registration.py        # register() — feeds / exchange_data 注册
├── __init__.py                    # 包导出
├── exchange_data/
│   └── __init__.py              # BitmartExchangeData, BitmartExchangeDataSpot
├── feeds/
│   └── live_bitmart/
│       ├── __init__.py          # 模块导出
│       ├── spot.py              # BitmartRequestDataSpot — 所有 SPOT REST 端点
│       └── request_base.py       # BitmartRequestData — 带签名逻辑的基类
├── containers/
│   ├── __init__.py
│   ├── orders/__init__.py
│   ├── balances/__init__.py
│   ├── accounts/__init__.py
│   ├── bars/__init__.py
│   ├── tickers/__init__.py
│   └── orderbooks/__init__.py
└── errors/
    └── __init__.py
```

---

## 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **市场数据** | `get_ticker` / `get_tick` | 24小时滚动行情 |
| | `get_depth` | 订单簿深度（最大50档） |
| | `get_kline` / `get_bars` | K线（1分钟到1月） |
| | `get_trades` / `get_trade_history` | 近期成交历史 |
| | `get_server_time` | 服务器时间同步 |
| | `get_exchange_info` | 交易所交易对信息 |
| **账户** | `get_balance` | 资产余额 |
| | `get_account` | 完整账户信息 |
| **交易** | `make_order` | 下限价/市价单 |
| | `cancel_order` | 撤销订单 |
| | `query_order` | 按ID查询订单 |
| | `get_open_orders` | 所有挂单 |
| | `get_deals` | 订单成交历史 |

---

## BitMart API 详情

### 基础 URL

| 环境 | REST API | WebSocket |
|---|---|---|
| 生产环境 | `https://api-cloud.bitmart.com` | `wss://ws-manager-compress.bitmart.com/api?protocol=1.1` |

### 认证方式

BitMart API 使用 HMAC-SHA256 签名：

```
Message = timestamp#memo#body_str
Signature = HMAC-SHA256(api_secret, Message)
```

必需请求头：
- `X-BM-KEY` — API 密钥
- `X-BM-TIMESTAMP` — 毫秒级时间戳
- `X-BM-SIGN` — HMAC-SHA256 签名

### 交易对格式

BitMart 使用下划线格式：`BTCUSDT`、`ETHUSDT`

### K线周期

| 周期 | BitMart 代码 |
|---|---|
| 1分钟 | 1 |
| 3分钟 | 3 |
| 5分钟 | 5 |
| 15分钟 | 15 |
| 30分钟 | 30 |
| 45分钟 | 45 |
| 1小时 | 60 |
| 2小时 | 120 |
| 3小时 | 180 |
| 4小时 | 240 |
| 1天 | 1440 |
| 1周 | 10080 |
| 1月 | 43200 |

---

## 错误处理

所有 BitMart API 错误均翻译为 bt_api_base `ApiError` 子类。常见错误码：

| 代码 | 说明 |
|---|---|
| 1000 | 成功 |
| 50000-59999 | API 错误 |
| 50002 | 签名无效 |
| 50003 | API 密钥无效 |
| 50004 | 时间戳无效 |
| 50005 | 权限被拒绝 |
| 50006 | 请求过于频繁 |

---

## 限流配置

| 端点类型 | 限制 |
|---|---|
| 公开接口 | 200 请求/10秒 |
| 私有接口 | 100 请求/10秒 |
| 下单接口 | 200 请求/10秒 |

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-bitmart.readthedocs.io/ |
| **中文文档** | https://bt-api-bitmart.readthedocs.io/zh/latest/ |
| API 参考 | https://bt-api-bitmart.readthedocs.io/api/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bitmart/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com
