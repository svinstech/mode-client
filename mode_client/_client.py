import uuid
from base64 import b64encode
from datetime import datetime, timedelta, timezone
from typing import Optional, Literal, Dict, Any

import httpx
from pydantic import conint

from ._models import BatchQueries, Report, ReportRun


class ModeClient:
    def __init__(self, workspace: str, token: str, password: str) -> None:
        self._workspace = workspace
        self._auth = httpx.BasicAuth(token, password)

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

        r = self._request("POST", "signature_tokens", api="batch", json=data)

        bearer_token = b64encode(
            f"{r['token']}:{r['access_key']}:{r['access_secret']}".encode()
        ).decode()
        self._auth_header = {"Authorization": "Bearer " + bearer_token}

        self._signature_token_id = r["token"]

    def __enter__(self):
        return self

    def close(self) -> None:
        self._request(
            "DELETE", f"signature_tokens/{self._signature_token_id}", api="batch"
        )

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _request(
        self,
        method: str,
        resource: str,
        api: Literal["api", "batch"] = "api",
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any:
        url = f"https://app.mode.com/{api}/{self._workspace}/{resource}"

        auth = None
        if api == "api" or (api == "batch" and resource.startswith("signature_tokens")):
            auth = self._auth

        headers = None
        if api == "batch" and not resource.startswith("signature_tokens"):
            headers = self._auth_header

        r = httpx.request(
            method=method,
            url=url,
            json=json,
            auth=auth,
            params=params,
            headers=headers,
        )
        r.raise_for_status()
        return r.json()

    def get_report(self, report: str) -> Report:
        return Report.parse_obj(self._request("GET", f"reports/{report}"))

    def create_report_run(self, report: str, parameters: Dict[str, Any]) -> ReportRun:
        return ReportRun.parse_obj(
            self._request("POST", f"reports/{report}/runs", json=parameters)
        )

    def list_queries_for_account(
        self,
        page: conint(gt=0) = 1,
        per_page: conint(gt=0, le=1000) = 1000,
        include_spaces: Optional[Literal["all"]] = None,
    ) -> BatchQueries:
        params = {"page": page, "per_page": per_page}

        if include_spaces:
            params["include_spaces"] = include_spaces

        return BatchQueries.parse_obj(
            self._request("GET", "queries", api="batch", params=params)
        )
