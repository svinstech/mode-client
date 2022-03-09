from typing import List

from pydantic import BaseModel, parse_obj_as

from . import ModeBaseClient


class Parameters(BaseModel):
    status: List[str]
    policy_status: List[str]
    start_date: str
    end_date: str


class QueryRun(BaseModel):
    id: int
    token: str
    raw_source: str
    state: str
    created_at: str
    completed_at: str
    data_source_id: int
    limit: bool
    query_token: str
    query_name: str
    query_created_at: str
    parameters: Parameters
    rendered_source: str
    max_result_bytes: int


class ModeQueryRunClient(ModeBaseClient):
    async def get(self, report: str, run: str, query_run: str) -> QueryRun:
        return QueryRun.parse_obj(
            await self.request(
                "GET", f"reports/{report}/runs/{run}/query_runs/{query_run}"
            )
        )

    async def list(self, report: str, run: str) -> List[QueryRun]:
        response = await self.request("GET", f"reports/{report}/runs/{run}/query_runs")

        return parse_obj_as(List[QueryRun], response["_embedded"]["query_runs"])
