from json import JSONDecodeError
from typing import Optional, Dict, Any

import httpx


class ModeBaseClient:
    def __init__(self, client: httpx.Client):
        self.client = client

    def request(
        self,
        method: str,
        resource: str,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any:
        if params:
            params = {k: v for k, v in params.items() if v}

        response = self.client.request(method=method, url=resource, json=json, params=params)
        response.raise_for_status()

        try:
            return response.json()
        except JSONDecodeError:
            return response.text
