import httpx

from .clients import (
    ModeCollectionClient,
    ModeQueryClient,
    ModeQueryRunClient,
    ModeReportClient,
    ModeReportRunClient,
)


class ModeClient:
    def __init__(self, workspace: str, token: str, password: str):
        client = httpx.Client(
            base_url=f"https://app.mode.com/api/{workspace}",
            auth=httpx.BasicAuth(token, password),
            timeout=10.0,
        )

        self.collection = ModeCollectionClient(client)
        self.query = ModeQueryClient(client)
        self.query_run = ModeQueryRunClient(client)
        self.report = ModeReportClient(client)
        self.report_run = ModeReportRunClient(client)

        self._client = client

    def __enter__(self):
        return self

    def close(self):
        self._client.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
