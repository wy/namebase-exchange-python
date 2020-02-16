"""
ENUMS are listed in https://github.com/namebasehq/exchange-api-documentation/blob/master/rest-api.md
"""
__all__ = ['Symbol', 'Asset', 'OrderType', 'OrderSide', 'Interval']

from enum import Enum


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
    FIFTEEN_MINUTES = "5m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"


