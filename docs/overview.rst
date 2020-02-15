========
Overview
========

Introduction
^^^^^^^^^^^^

This library is intended to empower developers when interacting with the Namebase Exchange API by providing simple Python interfaces.

Namebase is the first Exchange for Handshake (HNS) and launched in Feb 2020 with the HNSBTC Trading pair.

The official Namebase Exchange API documentation can be found at https://github.com/namebasehq/exchange-api-documentation

API Requests
^^^^^^^^^^^^

The Namebase Exchange API uses REST architecture to server data through its endpoints.  The requests and responses of the endpoint use JSON format.

While the endpoint returns JSON this package turns the request into a Python dictionary for easier interoperability and function lookup.

All endpoints require authenticationt through the API Token.


Rate Limits
^^^^^^^^^^^

All endpoints are rate-limited by the Namebase team.  Hard and fast rules are not given.
