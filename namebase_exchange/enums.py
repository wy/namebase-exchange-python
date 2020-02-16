"""
ENUMS are listed in https://github.com/namebasehq/exchange-api-documentation/blob/master/rest-api.md
"""
__all__ = ['Symbol', 'Asset', 'OrderType', 'OrderSide', 'Interval', 'Endpoint']

from enum import Enum


class Endpoint(Enum):
    TRADES = '/ws/v0/stream/trades'
    KLINES_1m = '/ws/v0/ticker/kline_1m'
    KLINES_5m = '/ws/v0/ticker/kline_5m'
    KLINES_15m = '/ws/v0/ticker/kline_15m'
    KLINES_1h = '/ws/v0/ticker/kline_1h'
    KLINES_4h = '/ws/v0/ticker/kline_4h'
    KLINES_12h = '/ws/v0/ticker/kline_12h'
    KLINES_1d = '/ws/v0/ticker/kline_1d'
    KLINES_1w = '/ws/v0/ticker/kline_1w'
    PRICES = '/ws/v0/ticker/day'
    DEPTH = '/ws/v0/ticker/depth'


class Symbol(Enum):
    HNSBTC = "HNSBTC"


class Asset(Enum):
    HNS = "HNS"
    BTC = "BTC"


class OrderType(Enum):
    LIMIT = "LMT"
    MARKET = "MKT"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class Interval(Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"


