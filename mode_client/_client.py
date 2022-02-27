import uuid
from base64 import b64encode
from datetime import datetime, timedelta, timezone
from typing import Optional, Literal, Dict, Any

import httpx
from pydantic import conint

from ._models import BatchQueries, Report, ReportRun


class ModeClient:
    def __init__(
        self, workspace: str, token: str, password: str, batch: bool = False
    ) -> None:
        self._base_url = f"https://app.mode.com/api/{workspace}"
        self._auth = httpx.BasicAuth(token, password)
        self._batch = batch

        if self._batch:
            self._batch_base_url = f"https://app.mode.com/batch/{workspace}"
            data = {
                "signature_token": {
                    "name": str(uuid.uuid4()),
                    "expires_at": (
                        datetime.now(timezone.utc) + timedelta(days=1)
                    ).isoformat(),
                    "auth_scope": {
                        "authentication_for": "batch-api",
                        "authorization_type": "read-only",
                    },
                }
            }

            r = self._request(
                "POST",
                f"{self._batch_base_url}/signature_tokens",
                json=data,
                auth=self._auth,
            )

            bearer_token = b64encode(
                f"{r['token']}:{r['access_key']}:{r['access_secret']}".encode()
            ).decode()
            self._header = {"Authorization": "Bearer " + bearer_token}

            self._signature_token_id = r["token"]

    def __enter__(self):
        return self

    def close(self) -> None:
        if self._batch:
            self._request(
                "DELETE",
                f"{self._batch_base_url}/signature_tokens/{self._signature_token_id}",
                auth=self._auth,
            )

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @staticmethod
    def _request(method, url, json=None, auth=None, params=None, headers=None) -> Any:
        r = httpx.request(
            method=method, url=url, json=json, auth=auth, params=params, headers=headers
        )
        r.raise_for_status()
        return r.json()

    def get_report(self, report: str) -> Report:
        return Report.parse_obj(
            self._request("GET", f"{self._base_url}/reports/{report}", auth=self._auth)
        )

    def create_report_run(self, report: str, parameters: Dict[str, Any]) -> ReportRun:
        return ReportRun.parse_obj(
            self._request(
                "POST",
                f"{self._base_url}/reports/{report}/runs",
                json=parameters,
                auth=self._auth,
            )
        )

    def list_queries_for_account(
        self,
        page: conint(gt=0) = 1,
        per_page: conint(gt=0, le=1000) = 1000,
        include_spaces: Optional[Literal["all"]] = None,
    ) -> BatchQueries:
        assert (self._batch, "Batch Mode must be enabled to call this API")

        params = {"page": page, "per_page": per_page}

        if include_spaces:
            params["include_spaces"] = include_spaces

        return BatchQueries.parse_obj(
            self._request(
                "GET",
                f"{self._batch_base_url}/queries",
                params=params,
                headers=self._header,
            )
        )
