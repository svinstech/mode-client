from datetime import datetime
from typing import List

from pydantic import BaseModel, parse_obj_as

from . import ModeBaseClient


class Query(BaseModel):
    id: int
    token: str
    raw_query: str
    created_at: datetime
    updated_at: datetime
    name: str
    last_run_id: int
    data_source_id: int
    explorations_count: int
    report_imports_count: int


class ModeQueryClient(ModeBaseClient):
    def get(self, report: str, query: str) -> Query:
        return Query.parse_obj(
            self.request("GET", f"/reports/{report}/queries/{query}")
        )

    def list(self, report: str) -> List[Query]:
        response = self.request("GET", f"/reports/{report}/queries")

        return parse_obj_as(List[Query], response["_embedded"]["queries"])

    def create(
        self, report: str, raw_query: str, data_source_id: int, name: str
    ) -> Query:
        json = {
            "query": {
                "raw_query": raw_query,
                "data_source_id": data_source_id,
                "name": name,
            }
        }

        return Query.parse_obj(
            self.request("POST", f"/reports/{report}/queries", json=json)
        )

    def update(
        self, report: str, query: str, raw_query: str, data_source_id: int, name: str
    ) -> Query:
        json = {
            "query": {
                "raw_query": raw_query,
                "data_source_id": data_source_id,
                "name": name,
            }
        }

        return Query.parse_obj(
            self.request("PATCH", f"/reports/{report}/queries/{query}", json=json)
        )

    def delete(self, report: str, query: str) -> Query:
        return Query.parse_obj(
            self.request("DELETE", f"/reports/{report}/queries/{query}")
        )
