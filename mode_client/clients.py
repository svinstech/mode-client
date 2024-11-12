from __future__ import annotations

from json import JSONDecodeError
from typing import Any, Dict, List, Literal, Optional

import httpx
from pydantic import parse_obj_as

from mode_client.models import (
    Account,
    Query,
    QueryRun,
    Report,
    ReportRun,
    ReportRuns,
    Space,
    Definition,
)


class ModeBaseClient:
    def __init__(self, workspace: str, token: str, password: str):
        self.client = httpx.Client(
            base_url=f"https://app.mode.com/api/{workspace}",
            auth=httpx.BasicAuth(token, password),
            timeout=10.0,
        )

    def request(
        self,
        method: str,
        resource: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        if params:
            params = {k: v for k, v in params.items() if v}

        response = self.client.request(
            method=method, url=resource, json=json, params=params
        )
        response.raise_for_status()

        try:
            return response.json()
        except JSONDecodeError:
            return response.text


class ModeAccountClient(ModeBaseClient):
    def __init__(self, _: str, token: str, password: str):
        super().__init__("", token, password)

    def get(self, account: str) -> Account:
        response = self.request("GET", f"/{account}")

        return Account.parse_obj(response)


class ModeQueryClient(ModeBaseClient):
    def get(self, report: str, query: str) -> Query:
        response = self.request("GET", f"/reports/{report}/queries/{query}")

        return Query.parse_obj(response)

    def list(self, report: str) -> List[Query]:
        response = self.request("GET", f"/reports/{report}/queries")

        return parse_obj_as(List[Query], response["_embedded"]["queries"])

    def create(
        self, report: str, raw_query: str, data_source_id: int, name: str
    ) -> None:
        json = {
            "query": {
                "raw_query": raw_query,
                "data_source_id": data_source_id,
                "name": name,
            }
        }
        self.request("POST", f"/reports/{report}/queries", json=json)

    def update(
        self,
        report: str,
        query: str,
        raw_query: Optional[str] = None,
        data_source_id: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Query:
        raw_json = {
            "raw_query": raw_query,
            "data_source_id": data_source_id,
            "name": name,
        }
        json = {k: v for k, v in raw_json.items() if v is not None}

        response = self.request(
            "PATCH", f"/reports/{report}/queries/{query}", json={"query": json}
        )

        return Query.parse_obj(response)

    def delete(self, report: str, query: str) -> None:
        self.request("DELETE", f"/reports/{report}/queries/{query}")


class ModeQueryRunClient(ModeBaseClient):
    def get(self, report: str, run: str, query_run: str) -> QueryRun:
        response = self.request(
            "GET", f"/reports/{report}/runs/{run}/query_runs/{query_run}"
        )

        return QueryRun.parse_obj(response)

    def list(self, report: str, run: str) -> List[QueryRun]:
        response = self.request("GET", f"/reports/{report}/runs/{run}/query_runs")

        return parse_obj_as(List[QueryRun], response["_embedded"]["query_runs"])


class ModeReportClient(ModeBaseClient):
    def get(self, report: str) -> Report:
        response = self.request("GET", f"/reports/{report}")

        return Report.parse_obj(response)

    def list(self, space: str) -> List[Report]:
        params = {"order": "desc", "order_by": "updated_at"}
        response = self.request("GET", f"/spaces/{space}/reports", params=params)

        return parse_obj_as(List[Report], response["_embedded"]["reports"])

    def update(
        self,
        report: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        space_token: Optional[str] = None,
    ) -> Report:
        raw_json = {
            "name": name,
            "description": description,
            "space_token": space_token,
        }
        json = {k: v for k, v in raw_json.items() if v is not None}
        response = self.request("PATCH", f"/reports/{report}", json={"report": json})

        return Report.parse_obj(response)

    def delete(self, report: str) -> None:
        self.request("DELETE", f"/reports/{report}")

    def archive(self, report: str) -> Report:
        response = self.request("PATCH", f"/reports/{report}/archive")
        return Report.parse_obj(response)

    def unarchive(self, report: str) -> Report:
        response = self.request("PATCH", f"/reports/{report}/unarchive")

        return Report.parse_obj(response)

    def sync(self, report: str, commit_message: Optional[str] = None) -> Report:
        json = {"commit_message": commit_message}
        response = self.request("PATCH", f"/reports/{report}/sync_to_github", json=json)

        return Report.parse_obj(response)


class ModeReportRunClient(ModeBaseClient):
    def get(self, report: str, run: str) -> ReportRun:
        response = self.request("GET", f"/reports/{report}/runs/{run}")

        return ReportRun.parse_obj(response)

    def list(self, report: str) -> ReportRuns:
        params = {"order": "desc", "order_by": "updated_at"}
        raw_response = self.request("GET", f"/reports/{report}/runs", params=params)
        response = {
            "pagination": raw_response["pagination"],
            "report_runs": raw_response["_embedded"]["report_runs"],
        }

        return ReportRuns.parse_obj(response)

    def clone(self, report: str, run: str) -> ReportRun:
        response = self.request("POST", f"/reports/{report}/runs/{run}/clone")
        return ReportRun.parse_obj(response)

    def create(self, report: str, parameters: Dict[str, Any]) -> ReportRun:
        response = self.request(
            "POST", f"/reports/{report}/runs", json={"parameters": parameters}
        )
        return ReportRun.parse_obj(response)


class ModeSpaceClient(ModeBaseClient):
    def get(self, space: str) -> Space:
        response = self.request("GET", f"/spaces/{space}")
        return Space.parse_obj(response)

    def list(self, filter_: Literal["all", "custom"] = "custom") -> List[Space]:
        params = {"filter": filter_}
        response = self.request("GET", "/spaces", params=params)
        spaces = response["_embedded"]["spaces"]

        return parse_obj_as(List[Space], spaces)

    def create(self, name: str, description: str) -> Space:
        json = {"space": {"name": name, "description": description}}
        response = self.request("POST", "/spaces", json=json)

        return Space.parse_obj(response)

    def update(
        self, space: str, name: Optional[str] = None, description: Optional[str] = None
    ) -> Space:
        raw_json = {"name": name, "description": description}
        json = {k: v for k, v in raw_json.items() if v is not None}
        response = self.request("POST", f"/spaces/{space}", json={"space": json})

        return Space.parse_obj(response)

    def delete(self, space: str) -> None:
        self.request("DELETE", f"/spaces/{space}")


class ModeDefinitionClient(ModeBaseClient):
    def get(self, definition_token: str) -> Definition:
        response = self.request("GET", f"/definitions/{definition_token}")

        return Definition.parse_obj(response)

    def list(
        self, filter_: Optional[str] = None, tokens: Optional[List[str]] = None
    ) -> List[Definition]:
        params = {"filter": filter_, "tokens": tokens}
        response = self.request("GET", "/definitions", params=params)
        definitions = response["_embedded"]["definitions"]

        return parse_obj_as(List[Definition], definitions)

    def create(self, data: Dict[str, Any]) -> Definition:
        response = self.request("POST", "/definitions", json={"definition": data})

        return Definition.parse_obj(response)

    def update(self, definition_token: str, data: Dict[str, Any]) -> Definition:
        data = {k: v for k, v in data.items() if v is not None}
        response = self.request(
            "POST", f"/definitions/{definition_token}", json={"definition": data}
        )

        return Definition.parse_obj(response)

    def delete(self, definition_token: str) -> None:
        self.request("DELETE", f"definitions/{definition_token}")

    def sync(
        self, definition_token: str, commit_message: Optional[str] = None
    ) -> Definition:
        json = {"commit_message": commit_message}
        response = self.request(
            "PATCH", f"/definitions/{definition_token}/sync_to_github", json=json
        )

        return Definition.parse_obj(response)


class ModeClient:
    def __init__(self, workspace: str, token: str, password: str):
        self.workspace = workspace
        self.token = token
        self.password = password

    @property
    def account(self) -> ModeAccountClient:
        return ModeAccountClient(self.workspace, self.token, self.password)

    @property
    def query(self) -> ModeQueryClient:
        return ModeQueryClient(self.workspace, self.token, self.password)

    @property
    def query_run(self) -> ModeQueryRunClient:
        return ModeQueryRunClient(self.workspace, self.token, self.password)

    @property
    def report(self) -> ModeReportClient:
        return ModeReportClient(self.workspace, self.token, self.password)

    @property
    def report_run(self) -> ModeReportRunClient:
        return ModeReportRunClient(self.workspace, self.token, self.password)

    @property
    def space(self) -> ModeSpaceClient:
        return ModeSpaceClient(self.workspace, self.token, self.password)

    @property
    def definition(self) -> ModeDefinitionClient:
        return ModeDefinitionClient(self.workspace, self.token, self.password)
