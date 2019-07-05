import logging
import os
from datetime import datetime
from urllib.parse import urljoin

import requests

from .exceptions import ResourceUnavailable, TokenError, Unauthorized

logging.basicConfig(level=logging.DEBUG)

__all__ = ("Client",)


class Client:
    def __init__(self, client_id=None, client_secret=None, audience=None):
        self.client = requests.session()
        self.client_id = client_id or os.environ.get("CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("CLIENT_SECRET")
        self.audience = audience or os.environ.get("AUDIENCE")

    def get_token(self):
        token = os.environ.get("{{ cookiecutter.package_name }}-token")
        expire = os.environ.get("{{ cookiecutter.package_name }}-token-expire")
        now = datetime.now().timestamp()
        if expire is None or (now - float(expire)) >= 36000:
            token = self._fetch_token(self.client_id, self.client_secret, self.audience)
            os.environ["{{ cookiecutter.package_name }}-token"] = token
            os.environ["{{ cookiecutter.package_name }}-token-expire"] = str(now)
        return token

    def _fetch_token(self, client_id, client_secret, audience):
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": audience,
            "grant_type": "client_credentials",
        }
        resp = self.client.post(TOKEN_URL, data=payload)
        if resp.status_code != 200:
            raise TokenError(resp.json())
        return resp.json()["access_token"]

    def get_json(self, url, query_params=None):
        _url = urljoin(API_URL, url)

        logging.debug("get_json ({}): {}".format(_url, query_params))
        token = self.get_token()
        query_params = query_params or dict()
        headers = {"Authorization": "Bearer {}".format(token)}
        resp = self.client.get(_url, params=query_params, headers=headers)

        if resp.status_code == 401:
            raise Unauthorized(resp.text)
        elif resp.status_code != 200:
            raise ResourceUnavailable(resp.text)

        return resp.json()

    def get_paginated_json(self, url, query_params=None):
        query_params = query_params or dict()
        data = self.get_json(url, query_params)
        next_url = data.get("next")
        for rec in data.get("results") or []:
            yield rec

        if next_url:
            yield from self.get_paginated_json(next_url)
