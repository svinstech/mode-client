from typing import Any, Dict, Optional, Literal, List

from pydantic import BaseModel

from . import ModeBaseClient


class ReportRun(BaseModel):
    token: str
    state: Literal[
        "pending",
        "enqueued",
        "cancelled",
        "failed",
        "succeeded",
        "completed",
        "running_notebook",
    ]
    parameters: Dict[str, Any]
    created_at: Any
    updated_at: Any
    completed_at: Any
    purge_started_at: Any
    purge_completed_at: Any
    python_state: Literal["none", "pending", "failed", "submitted", "succeeded"]
    form_fields: List[Any]


class Pagination(BaseModel):
    page: int
    per_page: int
    count: int
    total_pages: int
    total_count: int


class ReportRunList(BaseModel):
    pagination: Pagination
    report_runs: List[ReportRun]


class ModeReportRunClient(ModeBaseClient):
    def get(self, report: str, run: str) -> ReportRun:
        return ReportRun.parse_obj(self.request("GET", f"/reports/{report}/runs/{run}"))

    def list(
        self,
        report: str,
        filter_: Optional[str] = None,
        order: Literal["asc", "desc"] = "desc",
        order_by: Literal["created_at", "updated_at"] = "updated_at",
    ) -> ReportRunList:
        params = {"filter": filter_, "order": order, "order_by": order_by}

        return ReportRunList.parse_obj(
            self.request("GET", f"/reports/{report}/runs", params=params)
        )

    def clone(self, report: str, run: str) -> ReportRun:
        return ReportRun.parse_obj(
            self.request("POST", f"/reports/{report}/runs/{run}/clone")
        )

    def create(self, report: str, json: Dict[str, Any]) -> ReportRun:
        return ReportRun.parse_obj(
            self.request("POST", f"/reports/{report}/runs", json=json)
        )
