Namebase Exchange Api for Python
==

Python 3.6+ client for interacting with Namebase Exchange API.

## Usage

All requests require an API key. You can generate a key from https://www.namebase.io/pro.

At the time of writing, all documented API keys are supported. This may change at any time.
See the raw API documentation calls: https://github.com/namebasehq/exchange-api-documentation/

On top of the raw APIs, we also provide the convenience functions:
- market_buy: Market Buy
- market_sell: Market Sell
- limit_buy: Limit Buy
- limit_sell: Limit Sell

## Installation

### Requirements

- Python 3.6 or greater

### Install

> from namebase_exchange import *
>
> exchange = Exchange(YOUR_API_KEY, YOUR_SECRET_KEY)
>
> exchange.get_depth(Symbol.HNSBTC)
>
> exchange.market_sell(Symbol.HNSBTC, 500)

