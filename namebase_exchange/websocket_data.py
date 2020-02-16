from typing import Callable, Type
import websocket
from websocket import WebSocketApp
from namebase_exchange.enums import Endpoint

"""
Simple default functions to print out the message.
Can do more complicated things as needed.
"""


def _on_message(ws, message):
    print(message)


def _on_error(ws, error):
    print(error)


def _on_close(ws):
    print("### closed ###")


class ExchangeWS:
    base_wss_url = "wss://app.namebase.io:443"

    def __init__(self, endpoint: Endpoint,
                 on_message: Callable[[Type[WebSocketApp], str], None] = _on_message,
                 on_error: Callable[[Type[WebSocketApp], str], None] = _on_error,
                 on_close: Callable[[Type[WebSocketApp], str], None] = _on_close
                 ):
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close

        self.ws = websocket.WebSocketApp(self.base_wss_url + endpoint.value,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()
