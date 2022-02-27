import uuid
from base64 import b64encode
from datetime import datetime, timedelta, timezone
from typing import Optional, Literal, Dict, Union

import httpx

from ._models import BatchQueries, Report, ReportRun


class ModeClient:
    def __init__(self,
                 workspace: str,
                 token: str,
                 password: str,
                 batch: bool = False
                 ) -> None:
        self._base_url = f"https://app.mode.com/api/{workspace}"
        self._auth = httpx.BasicAuth(token, password)
        self._batch = batch

        if self._batch:
            self._batch_base_url = f"https://app.mode.com/batch/{workspace}"
            data = {
                "signature_token": {
                    "name": str(uuid.uuid4()),
                    "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
                    "auth_scope": {"authentication_for": "batch-api", "authorization_type": "read-only"}
                }
            }

            r = httpx.post(f"{self._batch_base_url}/signature_tokens", json=data, auth=self._auth)
            r.raise_for_status()

            rj = r.json()

            bearer_token = b64encode(f"{rj['token']}:{rj['access_key']}:{rj['access_secret']}".encode()).decode()
            self._header = {"Authorization": "Bearer " + bearer_token}

            self._signature_token_id = rj['token']

    def __enter__(self):
        return self

    def close(self) -> None:
        if self._batch:
            r = httpx.delete(f"{self._batch_base_url}/signature_tokens/{self._signature_token_id}", auth=self._auth)
            r.raise_for_status()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def get_report(self, report: str) -> Report:
        r = httpx.get(f"{self._base_url}/reports/{report}", auth=self._auth)
        r.raise_for_status()
        return Report.parse_obj(r.json())

    def create_report_run(self, report: str, parameters: Dict[str, Union[str, int]]) -> ReportRun:
        r = httpx.post(f"{self._base_url}/reports/{report}/runs", json=parameters, auth=self._auth)
        r.raise_for_status()
        return ReportRun.parse_obj(r.json())

    def list_queries_for_account(self,
                                 include_spaces: Optional[Literal['all']] = None,
                                 per_page: int = 1000
                                 ) -> BatchQueries:
        assert(self._batch, "Batch Mode must be enabled to call this API")

        params = {'per_page': per_page}

        if include_spaces:
            params['include_spaces'] = include_spaces

        r = httpx.get(f"{self._batch_base_url}/queries", params=params, headers=self._header)
        r.raise_for_status()

        return BatchQueries.parse_obj(r.json())
