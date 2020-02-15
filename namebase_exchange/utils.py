"""
Includes Request class for convenience which applies consistent Timeout, Headers and Base URL settings.
"""
__all__ = ['get_current_time_milliseconds', 'encode_credentials', 'Request']

import base64
import requests
import time


def get_current_time_milliseconds():
    return round(time.time() * 1000)


def encode_credentials(access_key: str, secret_key: str) -> str:
    return (base64.b64encode('{}:{}'.format(access_key, secret_key).encode("utf-8"))).decode("utf-8")


class Request(object):

    def __init__(self, api_base_url, headers, timeout=30):
        self.url = api_base_url
        self.timeout = timeout
        self.headers = headers

    def get(self, path, params=None):
        """Perform GET request"""
        r = requests.get(url=self.url + path, params=params, timeout=self.timeout,
                         headers=self.headers)
        r.raise_for_status()
        return r.json()

    def post(self, path, data=None, json_data=None, params=None):
        """Perform POST request"""
        r = requests.post(url=self.url + path, data=data, json=json_data, params=params, timeout=self.timeout,
                          headers=self.headers)
        r.raise_for_status()
        return r.json()

    def delete(self, path, json_data=None, params=None):
        """Perform DELETE request"""
        r = requests.delete(url=self.url + path, params=params, json=json_data, timeout=self.timeout,
                            headers=self.headers)
        r.raise_for_status()
        return r.json()

    def status(self):
        r = requests.get(url=self.url + "/info", headers=self.headers)
        r.raise_for_status()
        return r.json()
