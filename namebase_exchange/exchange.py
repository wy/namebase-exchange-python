# -*- coding:utf-8 -*-
"""
Description:
    Implements Python client library for Namebase Exchange API.
    All calls require Authentication through a Bearer Token.
Usage:
    from namebase_exchange.exchange import *
"""
from typing import Optional
from namebase_exchange.enums import *
from namebase_exchange.utils import *

__all__ = ['Exchange', 'Symbol', 'Asset', 'OrderType', 'OrderSide', 'Interval']

DEFAULT_API_ROOT = "https://www.namebase.io/api"
DEFAULT_API_VERSION = "/v0"


class Exchange:

    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 api_root=DEFAULT_API_ROOT,
                 api_version=DEFAULT_API_VERSION):
        headers = {
            "Authorization": "Basic {}".format(encode_credentials(access_key, secret_key)),
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }

        print(headers)

        self.request = Request(api_base_url=api_root + api_version,
                               headers=headers,
                               timeout=30)

    def get_exchange_info(self):
        """
        Function to fetch the Current Exchange trading rules and symbol information.
        Use to test connectivity to the Rest API. Execution of this function is as follows::

            get_exchange_info()

        The expected return result::

            {
                "timezone": "UTC",
                "serverTime": 1555556529865,
                "symbols": [{
                    "symbol": "HNSBTC",
                    "status": "TRADING",
                    "baseAsset": "HNS",
                    "basePrecision": 6,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "orderTypes": ["LMT", "MKT"]
                }]
            }

        """
        return self.request.get(path="/info")

    def get_depth(self, symbol: Symbol, limit: int = 100) -> dict:
        """
        Function to get the Order Book Depth for a given Symbol. Execution of this function is as follows::

            get_exchange_depth(symbol=Symbol.HNSBTC, limit=100)

        The expected return result::

            {
                "lastEventId": 6828,         // The last event id this includes
                "bids": [
                    ["0.00003000",  "200.000000"] // [Price level, Quantity]
                ],
                "asks": [
                    ["0.00003100", "100.000000"]
                ]
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param limit: The max number of rows to return, default 100.
        :type limit: int
        :return: JSON Dictionary

        """
        api_params = {
            "symbol": symbol.value,
            "limit": limit
        }
        return self.request.get(path="/depth", params=api_params)

    def get_trade(self, symbol: Symbol, trade_id: Optional[int] = None, limit: int = 100,
                  receive_window: Optional[int] = None) -> dict:
        """
        Function to get older trades. Execution of this function is as follows::

            get_trade(symbol=Symbol.HNSBTC, trade_id=28457, limit=100)

        The expected return result::

            [
                {
                    "tradeId": 28457,
                    "price": "0.00003000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01500000",
                    "createdAt": 1555556529865,
                    "isBuyerMaker": true
                }
            ]

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param trade_id: The Trade ID (int) - not mandatory.
        :type trade_id: int
        :param limit: Limit on number of rows to return - default 100.
        :type limit: int
        :param receive_window: Receive Window - not mandatory.
        :type receive_window: int
        :return: List of trades

        """
        api_params = {
            "symbol": symbol.value,
            "limit": limit,
            "timestamp": get_current_time_milliseconds()
        }
        if trade_id is not None:
            api_params['tradeId'] = trade_id

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/trade', params=api_params)

    def get_kline(self, symbol: Symbol, interval: Interval, start_time: Optional[int] = None,
                  end_time: Optional[int] = None, limit: int = 100):
        """
        Function to get Kline (candlestick) bars for a given symbol. Execution of this function is as follows::

            get_kline(symbol=Symbol.HNSBTC, interval=Interval.ONE_HOUR, limit=100)

        The expected return result::

            [
                {
                    "openTime": 1557190800000,
                    "closeTime": 1557190859999,
                    "openPrice": "0.00002247",
                    "highPrice": "0.00002256",
                    "lowPrice": "0.00002243",
                    "closePrice": "0.00002253",
                    "volume": "10.001301",
                    "quoteVolume": "0.000224824",
                    "numberOfTrades": 42
                }
            ]

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param interval: The Kline Interval.
        :type interval: Interval
        :param start_time: Optional Start Time.
        :type start_time: int
        :param end_time: Optional End Time.
        :type end_time: int
        :param limit: Limit number of rows to be returned. Default 100.
        :type limit: int
        :return: List of Candlestick Bars.

        """
        api_params = {
            "symbol": symbol.value,
            "interval": interval,
            "limit": limit
        }

        if start_time is not None:
            api_params['startTime'] = start_time

        if end_time is not None:
            api_params['endTime'] = end_time

        return self.request.get(path='/ticker/klines', params=api_params)

    def get_ticker_day(self, symbol: Symbol):
        """
        Function to get 24 hour rolling window price change statistics. Execution of this function is as follows::

            get_ticker_day(symbol=Symbol.HNSBTC)

        The expected return result::

            {
                "volumeWeightedAveragePrice": "0.00001959",
                "priceChange": "0.00000019",
                "priceChangePercent": "0.8528",
                "openPrice": "0.00002228",
                "highPrice": "0.00002247",
                "lowPrice": "0.00001414",
                "closePrice": "0.00002247",
                "volume": "11413.935399",
                "quoteVolume": "0.22363732",
                "openTime": 1555467560001,
                "closeTime": 1555553960000,
                "firstTradeId": 19761,
                "lastTradeId": 20926,
                "numberOfTrades": 1166
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :return: JSON Dictionary

        """
        api_params = {
            "symbol": symbol.value
        }

        return self.request.get(path='/ticker/day', params=api_params)

    def get_ticker_price(self, symbol: Symbol):
        """
        Function to get latest price for a symbol or symbols. Execution of this function is as follows::

            get_ticker_price(symbol=Symbol.HNSBTC)

        The expected return result::

            {
                "price": "0.00002300"
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :return: JSON Dictionary

        """
        api_params = {
            "symbol": symbol.value
        }

        return self.request.get(path='/ticker/price', params=api_params)

    def get_ticker_book(self, symbol: Symbol):
        """
        Function to get best price/quantity on the order book for a symbol or symbols.
        Execution of this function is as follows::

            get_ticker_book(symbol=Symbol.HNSBTC)

        The expected return result::

            {
                "bidPrice": "0.00002000",
                "bidQuantity": "100.000000",
                "askPrice": "0.00002300",
                "askQuantity": "9000.100000"
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :return: JSON Dictionary
        """
        api_params = {
            "symbol": symbol.value
        }

        return self.request.get(path='/ticker/book', params=api_params)

    def get_ticker_supply(self, asset: Asset):
        """
        Function to get the circulating supply for the provided asset. Execution of this function is as follows::

            get_ticker_supply(asset=Asset.HNS)

        The expected return result::

            {
                "height": 22012,
                "circulatingSupply": "116082412.354562",
            }

        :param asset: Trading Asset.
        :type asset: Asset
        :return: JSON Dictionary

        """
        api_params = {
            "asset": asset.value
        }

        return self.request.get(path='/ticker/supply', params=api_params)

    def new_order(self, symbol: Symbol, side: OrderSide, order_type: OrderType, quantity: float,
                  price: Optional[float] = None,
                  receive_window: Optional[int] = None):
        """
        Function to send in a new order. Price is only required for Limit orders.
        Execution of this function is as follows::

            new_order(symbol=Symbol.HNSBTC, side=OrderSide.SELL, type=OrderType.MARKET,
            quantity=1000.0)

        The expected return result::

            {
                "orderId": 174,
                "createdAt": 1555556529865,
                "price": "0.00000000",
                "originalQuantity": "1000.00000000",
                "executedQuantity": "1000.00000000",
                "status": "FILLED",
                "type": "MKT",
                "side": "SELL",
                "fills": [
                    {
                    "price": "0.00003000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01500000",
                    "commission": "0.00000750",
                    "commissionAsset": "BTC"
                    },
                    {
                    "price": "0.00002000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01000000",
                    "commission": "0.00000500",
                    "commissionAsset": "BTC"
                    }
                ]
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param side: The desired Order Side.
        :type side: OrderSide
        :param order_type: The desired type of Order.
        :type order_type: OrderType
        :param quantity: The quantity of the base asset.
        :type quantity: float
        :param price: The price of the quote asset per 1 unit of base asset. Only mandatory for LIMIT orders.
        :type price: float
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary of immediate Order Status
        """
        api_params = {
            'symbol': symbol.value,
            'side': side.value,
            'type': order_type.value,
            'quantity': quantity,
            'timestamp': get_current_time_milliseconds()
        }

        if price is not None:
            api_params['price'] = price

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.post(path='/order', json_data=api_params)

    def get_order(self, symbol: Symbol, order_id: int,
                  receive_window: Optional[int] = None):
        """
        Function to get an order's status. Execution of this function is as follows::

            get_order(symbol=Symbol, order_id=1)

        The expected return result::

            {
                "orderId": 1,
                "price": "0.1",
                "originalQuantity": "1.0",
                "executedQuantity": "0.0",
                "status": "NEW",
                "type": "LMT",
                "side": "BUY",
                "createdAt": 1555556529865,
                "updatedAt": 1555556529865
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param order_id: The Order ID.
        :type order_id: int
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary of Order Information
        """
        api_params = {
            "symbol": symbol.value,
            "orderId": order_id,
            "timestamp": get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/order', params=api_params)

    def delete_order(self, symbol: Symbol, order_id: int,
                     receive_window: Optional[int] = None):
        """
        Function to cancel an active order. Execution of this function is as follows::

            delete_order(symbol=Symbol, order_id=1)

        The expected return result::

            {
                "orderId": 28,
                "price": "1.00000000",
                "originalQuantity": "910.00000000",
                "executedQuantity": "19.00000000",
                "status": "CANCELED",
                "type": "LMT",
                "side": "SELL",
                "createdAt": 1555556529865,
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param order_id: The Order ID.
        :type order_id: int
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary of Order Status.
        """
        api_params = {
            "symbol": symbol.value,
            "orderId": order_id,
            "timestamp": get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.delete(path='/order', json_data=api_params)

    def get_open_orders(self, symbol: Symbol, receive_window: Optional[int] = None):
        """
        Function to get the most recent open orders on a symbol (limited to 500).
        Execution of this function is as follows::

            get_open_orders(symbol=Symbol)

        The expected return result::

            [
                {
                    "orderId": 1,
                    "price": "0.1",
                    "originalQuantity": "1.0",
                    "executedQuantity": "0.0",
                    "status": "NEW",
                    "type": "LMT",
                    "side": "BUY",
                    "createdAt": 1555556529865,
                    "updatedAt": 1555556529865
                }
            ]

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary
        """
        api_params = {
            "symbol": symbol.value,
            "timestamp": get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/order/open', params=api_params)

    def get_all_orders(self, symbol: Symbol, order_id: Optional[int] = None,
                       limit: int = 100, receive_window: Optional[int] = None):
        """
        Function to get all account orders; active, cancelled, or filled.
        If order_id is provided, it will get orders >= order_id.
        Otherwise you will receive the most recent orders.
        Execution of this function is as follows::

            get_all_orders(symbol=Symbol, limit=100)

        The expected return result::

            [
                {
                    "orderId": 1,
                    "price": "0.1",
                    "originalQuantity": "1.0",
                    "executedQuantity": "0.0",
                    "status": "NEW",
                    "type": "LMT",
                    "side": "BUY",
                    "createdAt": 1555556529865,
                    "updatedAt": 1555556529865
                }
            ]

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param order_id: The Order ID.
        :type order_id: int
        :param limit: Limit number of rows. Default 100.
        :type limit: int
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: List of All Orders.
        """
        api_params = {
            "symbol": symbol.value,
            "limit": limit,
            "timestamp": get_current_time_milliseconds()
        }

        if order_id is not None:
            api_params['orderId'] = order_id

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/order/all', params=api_params)

    def get_account_information(self, receive_window: Optional[int] = None):
        """
        Function to get basic account information. Execution of this function is as follows::

            get_account_information()

        The expected return result::

            {
                "makerFee": 15, // in basis points, 0.15%
                "takerFee": 15, // in basis points, 0.15%
                "canTrade": true,
                "balances": [
                    {
                        "asset": "HNS",
                        "unlocked": "779.900092",
                        "lockedInOrders": "100.000000",
                        "canDeposit": true,
                        "canWithdraw": true
                    },
                    {
                        "asset": "BTC",
                        "unlocked": "5.10000012",
                        "lockedInOrders": "1.000000",
                        "canDeposit": true,
                        "canWithdraw": true
                    }
                ]
            }

        :param receive_window: Optional Receive Window
        :type receive_window: int
        :return: JSON Dictionary
        """
        api_params = {
            "timestamp": get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/account', params=api_params)

    def get_account_limits(self, receive_window: Optional[int] = None):
        """
        Function to get your account's withdrawal limits for all assets.
        Withdrawal limits are applied on a 24-hour rolling basis.
        Start and End time is provided in the response startTime and endTime.

        totalWithdrawn: how much asset has been withdrawn in past 24 hours.
        withdrawalLimit: how much can be withdrawn in the specified period.

        Execution of this function is as follows::

            get_account_limits()

        The expected return result::

            {
                "startTime": 1555467560001,
                "endTime": 1555553960000,
                "withdrawalLimits": [
                    {
                        "asset": "HNS",
                        "totalWithdrawn": "500.000000",
                        "withdrawalLimit": "10000.000000",
                    },
                    {
                        "asset": "BTC",
                        "totalWithdrawn": "0.50000000",
                        "withdrawalLimit": "5.00000000",
                    }
                ]
            }

        :param receive_window: Optional Receive Window
        :type receive_window: int
        :return: JSON Dictionary

        """
        api_params = {
            "timestamp": get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/account/limits', params=api_params)

    def get_account_trades(self, symbol: Symbol, trade_id: Optional[int],
                           limit: int = 100, receive_window: Optional[int] = None):
        """
        Function to get trades a specific account and symbol.

        If trade_id is set, it will get trades >= trade_id. Otherwise you will get your most recent trades.

        Execution of this function is as follows::

            get_account_trades(symbol=Symbol.HNSBTC)

        The expected return result::

            [
                {
                    "tradeId": 10921,
                    "orderId": 61313,
                    "price": "8.00000000",
                    "quantity": "200.000000",
                    "quoteQuantity": "1600.00000000",
                    "commission": "4.500000",
                    "commissionAsset": "HNS",
                    "createdAt": 1555556529865,
                    "isBuyer": true,
                    "isMaker": false,
                }
            ]

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param trade_id: The Trade ID.
        :type trade_id: int
        :param limit: Limit number of rows. Default 100.
        :type limit: int
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: List of Account Trades
        """
        api_params = {
            "symbol": symbol.value,
            "limit": limit,
            "timestamp": get_current_time_milliseconds()
        }

        if trade_id is not None:
            api_params['tradeId'] = trade_id

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/trade/account', params=api_params)

    def get_order_trades(self, symbol: Symbol, order_id: int,
                         receive_window: Optional[int] = None):
        """
        Function to get trades a specific order and symbol.
        Execution of this function is as follows::

            get_order_trades(symbol=Symbol.HNSBTC, order_id=61313)

        The expected return result::

            [
                {
                    "tradeId": 10921,
                    "orderId": 61313,
                    "price": "8.00000000",
                    "quantity": "200.000000",
                    "quoteQuantity": "1600.00000000",
                    "commission": "4.500000",
                    "commissionAsset": "HNS",
                    "createdAt": 1555556529865,
                    "isBuyer": true,
                    "isMaker": false,
                }
            ]

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param order_id: The Order ID.
        :type order_id: int
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: List of Trades

        """
        api_params = {
            "symbol": symbol.value,
            "orderId": order_id,
            "timestamp": get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/trade/order', params=api_params)

    def generate_deposit_address(self, asset: Asset,
                                 receive_window: Optional[int] = None):
        """
        Function to generate a deposit address.
        Execution of this function is as follows::

            generate_deposit_address(asset=Symbol.HNS)

        The expected return result::

            {
                "address": "ts1qjg8chhk2t4zff4ltdaug3g9f7sxgne98jyv6ar",
                "success": true,
                "asset": "HNS"
            }

        :param asset: The Trading Asset.
        :type asset: Asset
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary

        """
        api_params = {
            'asset': asset.value,
            'timestamp': get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.post(path='/deposit/address', json_data=api_params)

    def withdraw(self, asset: Asset, address: str, amount: float,
                 receive_window: Optional[int] = None):

        """
        Function to withdraw asset.
        Execution of this function is as follows::

            withdraw(asset=Symbol.HNS, address=YOUR_ADDRESS, amount=1932.1)

        The expected return result::

            {
                "message": "success",
                "success": true,
                "id": "df7282ad-df8c-44f7-b747-5b09079ee852"
            }

        :param asset: The Trading Asset.
        :type asset: Asset
        :param address: The Address where the Asset is to be withdrawn.
        :type address: str
        :param amount: The amount of asset to be withdrawn.
        :type amount: float
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary
        """
        api_params = {
            'asset': asset.value,
            'address': address,
            'amount': amount,
            'timestamp': get_current_time_milliseconds()
        }

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.post(path='/withdraw', json_data=api_params)

    def get_deposit_history(self, asset: Asset, start_time: Optional[int] = None,
                            end_time: Optional[int] = None, receive_window: Optional[int] = None):
        """
        Function to get deposit history for an asset.
        Execution of this function is as follows::

            get_deposit_history(asset=Symbol.HNS)

        The expected return result::

            [
                {
                    "asset": "HNS",
                    "amount": "31.853300",
                    "address": "ts1qtq6ymgcep8mz2ag32ftrktwws0hr4uygprjurf",
                    "txHash": "e7714680a4d93e3b29348eab38c22bb99949ed4d8aea7006091ff5f9712d1ec6",
                    "createdAt": 1555556529865,
                },
                {
                    "asset": "HNS",
                    "amount": "210.000333",
                    "address": "n1M5Rw3r7WkujB2dG1L84M3a4pzr2NKvfp",
                    "txHash": "1d0827c642bd67781f80fe15c0fbb349aa4e35117adba06a52add4b207d334dd",
                    "createdAt": 1555556529865,
                }
            ]

        :param asset: The Trading Asset.
        :type asset: Asset
        :param start_time: The Start Time.
        :type start_time: int
        :param end_time: The End Time.
        :type end_time: int
        :param receive_window: Optional Receive Window
        :type receive_window: int
        :return: List of Asset Deposits

        """
        api_params = {
            "asset": asset.value,
            "timestamp": get_current_time_milliseconds()
        }

        if start_time is not None:
            api_params['startTime'] = start_time

        if end_time is not None:
            api_params['endTime'] = end_time

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/deposit/history', params=api_params)

    def get_withdraw_history(self, asset: Asset, start_time: Optional[int] = None,
                             end_time: Optional[int] = None, receive_window: Optional[int] = None):
        """
        Function to get withdraw history for an asset.
        Execution of this function is as follows::

            get_withdraw_history(asset=Symbol.HNS)

        The expected return result::

            [
                {
                    "id": "3333edc6-e5c6-4d23-bf84-7b1072a90e37",
                    "asset": "HNS",
                    "amount": "1.000000",
                    "minerFee": "0.100000",
                    "address": "ts1qtq6ymgcep8mz2ag32ftrktwws0hr4uygprjurf",
                    "txHash": "e7714680a4d93e3b29348eab38c22bb99949ed4d8aea7006091ff5f9712d1ec6",
                    "createdAt": 1555556529865,
                },
                {
                    "id": "180ceb4d-d303-4fed-9af6-213b5137255a",
                    "asset": "HNS",
                    "amount": "1200.000000",
                    "minerFee": "0.200000",
                    "address": "ts1qygv5nh38e9sl8npm4pcx8mqqqfp9sjaq4jrsn5",
                    "txHash": "c5c398802554b861bef2ec7c4805846ff400a90f71059619974685848bbc4fd3",
                    "createdAt": 1555556529865,
                }
            ]

        :param asset: The Trading Asset.
        :type asset: Asset
        :param start_time: The Start Time.
        :type start_time: int
        :param end_time: The End Time.
        :type end_time: int
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: List of Withdraws

        """
        api_params = {
            "asset": asset.value,
            "timestamp": get_current_time_milliseconds()
        }

        if start_time is not None:
            api_params['startTime'] = start_time

        if end_time is not None:
            api_params['endTime'] = end_time

        if receive_window is not None:
            api_params['receiveWindow'] = receive_window

        return self.request.get(path='/withdraw/history', params=api_params)

    def limit_sell(self, symbol: Symbol, price: float, quantity: int,
                   receive_window: Optional[int]):
        """
        Function to execute a Limit Sell.
        Execution of this function is as follows::

            limit_sell(symbol=Symbol.HNSBTC, price=0.6,
            quantity=1000.0)

        The expected return result::

            {
                "orderId": 174,
                "createdAt": 1555556529865,
                "price": "0.6",
                "originalQuantity": "1000.00000000",
                "executedQuantity": "1000.00000000",
                "status": "FILLED",
                "type": "LMT",
                "side": "SELL",
                "fills": [
                    {
                    "price": "0.6000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01500000",
                    "commission": "0.00000750",
                    "commissionAsset": "BTC"
                    },
                    {
                    "price": "0.6",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01000000",
                    "commission": "0.00000500",
                    "commissionAsset": "BTC"
                    }
                ]
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param quantity: The quantity of the base asset.
        :type quantity: float
        :param price: The price of the quote asset per 1 unit of base asset.
        :type price: float
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary of immediate Order Status
        """

        return self.new_order(symbol,
                              OrderSide.SELL,
                              OrderType.LIMIT,
                              quantity,
                              price,
                              receive_window)

    def limit_buy(self, symbol: Symbol, price: float, quantity: int,
                  receive_window: Optional[int]):
        """
        Function to execute a Limit Buy.
        Execution of this function is as follows::

            limit_buy(symbol=Symbol.HNSBTC, price=0.6,
            quantity=1000.0)

        The expected return result::

            {
                "orderId": 174,
                "createdAt": 1555556529865,
                "price": "0.6",
                "originalQuantity": "1000.00000000",
                "executedQuantity": "1000.00000000",
                "status": "FILLED",
                "type": "LMT",
                "side": "BUY",
                "fills": [
                    {
                    "price": "0.6000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01500000",
                    "commission": "0.00000750",
                    "commissionAsset": "BTC"
                    },
                    {
                    "price": "0.6",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01000000",
                    "commission": "0.00000500",
                    "commissionAsset": "BTC"
                    }
                ]
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param quantity: The quantity of the base asset.
        :type quantity: float
        :param price: The price of the quote asset per 1 unit of base asset.
        :type price: float
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary of immediate Order Status
        """

        return self.new_order(symbol,
                              OrderSide.BUY,
                              OrderType.LIMIT,
                              quantity,
                              price,
                              receive_window)

    def market_sell(self, symbol: Symbol, quantity: int,
                    receive_window: Optional[int]):
        """
        Function to execute a Market Sell.
        Execution of this function is as follows::

            market_sell(symbol=Symbol.HNSBTC, quantity=1000.0)

        The expected return result::

            {
                "orderId": 174,
                "createdAt": 1555556529865,
                "price": "0.0",
                "originalQuantity": "1000.00000000",
                "executedQuantity": "1000.00000000",
                "status": "FILLED",
                "type": "MKT",
                "side": "SELL",
                "fills": [
                    {
                    "price": "0.6000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01500000",
                    "commission": "0.00000750",
                    "commissionAsset": "BTC"
                    },
                    {
                    "price": "0.6000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01000000",
                    "commission": "0.00000500",
                    "commissionAsset": "BTC"
                    }
                ]
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param quantity: The quantity of the base asset.
        :type quantity: float
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary of immediate Order Status
        """
        return self.new_order(symbol,
                              OrderSide.SELL,
                              OrderType.MARKET,
                              quantity,
                              price=None,
                              receive_window=receive_window)

    def market_buy(self, symbol: Symbol, quantity: int,
                   receive_window: Optional[int]):
        """
        Function to execute a Market Buy.
        Execution of this function is as follows::

            market_buy(symbol=Symbol.HNSBTC, quantity=1000.0)

        The expected return result::

            {
                "orderId": 174,
                "createdAt": 1555556529865,
                "price": "0.0",
                "originalQuantity": "1000.00000000",
                "executedQuantity": "1000.00000000",
                "status": "FILLED",
                "type": "MKT",
                "side": "BUY",
                "fills": [
                    {
                    "price": "0.6000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01500000",
                    "commission": "0.00000750",
                    "commissionAsset": "BTC"
                    },
                    {
                    "price": "0.6000",
                    "quantity": "500.000000",
                    "quoteQuantity": "0.01000000",
                    "commission": "0.00000500",
                    "commissionAsset": "BTC"
                    }
                ]
            }

        :param symbol: The Trading Symbol.
        :type symbol: Symbol
        :param quantity: The quantity of the base asset.
        :type quantity: float
        :param receive_window: Optional Receive Window.
        :type receive_window: int
        :return: JSON Dictionary of immediate Order Status
        """
        return self.new_order(symbol,
                              OrderSide.BUY,
                              OrderType.MARKET,
                              quantity,
                              price=None,
                              receive_window=receive_window)
