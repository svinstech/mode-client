from typing import List

from pydantic import BaseModel, parse_obj_as

from . import ModeBaseClient


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
    rendered_source: str
    max_result_bytes: int


class ModeQueryRunClient(ModeBaseClient):
    def get(self, report: str, run: str, query_run: str) -> QueryRun:
        return QueryRun.parse_obj(
            self.request("GET", f"/reports/{report}/runs/{run}/query_runs/{query_run}")
        )

    def list(self, report: str, run: str) -> List[QueryRun]:
        response = self.request("GET", f"/reports/{report}/runs/{run}/query_runs")

        return parse_obj_as(List[QueryRun], response["_embedded"]["query_runs"])
