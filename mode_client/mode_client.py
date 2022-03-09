import aiohttp

from .clients import (
    ModeCollectionClient,
    ModeQueryClient,
    ModeQueryRunClient,
    ModeReportClient,
    ModeReportRunClient,
)


class ModeClient:
    def __init__(
        self, workspace: str, token: str, password: str, concurrent_connections: int = 5
    ):
        session = aiohttp.ClientSession(
            base_url=f"https://app.mode.com",
            auth=aiohttp.BasicAuth(token, password),
            connector=aiohttp.TCPConnector(limit=concurrent_connections),
        )

        self.collection = ModeCollectionClient(session, workspace)
        self.query = ModeQueryClient(session, workspace)
        self.query_run = ModeQueryRunClient(session, workspace)
        self.report = ModeReportClient(session, workspace)
        self.report_run = ModeReportRunClient(session, workspace)

        self._session = session

    async def __aenter__(self):
        return self

    async def _close(self):
        await self._session.close()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._close()
