from typing import Optional, Dict, Literal, Any

from aiohttp import ClientSession


class ModeBaseClient:
    def __init__(self, session: ClientSession, workspace: str):
        self.session = session
        self.workspace = workspace

    async def request(
        self,
        method: str,
        resource: str,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
        response_format: Literal["text", "json"] = "json",
    ) -> Any:
        if params:
            params = {k: v for k, v in params.items() if v}

        response = await self.session.request(
            method=method,
            url=f"/api/{self.workspace}/{resource}",
            json=json,
            params=params,
            raise_for_status=True,
        )
        return await getattr(response, response_format)()
