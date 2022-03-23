from datetime import datetime, timedelta, date
from typing import Any, Dict, Optional, Literal, List

from pydantic import BaseModel, parse_obj_as

from . import ModeBaseClient


class Report(BaseModel):
    token: str
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    edited_at: datetime
    theme_id: int
    color_mappings: Dict[str, Any]
    last_successful_sync_at: Optional[datetime]
    last_saved_at: Optional[datetime]
    archived: bool
    account_id: int
    account_username: str
    public: bool
    full_width: bool
    manual_run_disabled: bool
    run_privately: bool
    drilldowns_enabled: bool
    layout: str
    is_embedded: bool
    is_signed: bool
    shared: bool
    expected_runtime: float
    last_successfully_run_at: Optional[datetime]
    last_run_at: Optional[datetime]
    web_preview_image: Optional[str]
    last_successful_run_token: str
    query_count: str
    chart_count: str
    schedules_count: str
    query_preview: str
    description: str
    space_token: str
    flamingo_signature: str


class ModeReportClient(ModeBaseClient):
    def get(self, report: str) -> Report:
        return Report.parse_obj(self.request("GET", f"/reports/{report}"))

    def list(
        self,
        data_source: Optional[str] = None,
        space: Optional[str] = None,
        _filter: Optional[str] = None,
        order: Literal["asc", "desc"] = "desc",
        order_by: Literal["created_at", "updated_at"] = "updated_at",
    ) -> List[Report]:
        assert (
            bool(data_source) + bool(space) == 1
        ), "Only one of data_source, space can be defined"

        url = (
            f"/spaces/{space}/reports"
            if space
            else f"/data_sources/{data_source}/reports"
        )

        params = {"filter": _filter, "order": order, "order_by": order_by}
        response = self.request("GET", url, params=params)

        return parse_obj_as(List[Report], response["_embedded"]["reports"])

    def update(
        self, report: str, name: str, description: str, space_token: str
    ) -> Report:
        json = {"name": name, "description": description, "space_token": space_token}

        return Report.parse_obj(self.request("PATCH", f"/reports/{report}", json=json))

    def delete(self, report: str) -> None:
        self.request("DELETE", f"/reports/{report}")

    def archive(self, report: str) -> Report:
        return Report.parse_obj(self.request("PATCH", f"/reports/{report}/archive"))

    def purge(self, purge_date: date) -> None:
        assert purge_date < date.today() - timedelta(
            days=15
        ), "time cannot be within the past 15 days"
        json = {"time": purge_date.isoformat()}

        self.request("POST", "/reports/purge", json=json)

    def unarchive(self, report: str) -> Report:
        return Report.parse_obj(self.request("PATCH", f"/reports/{report}/unarchive"))

    def sync(self, report: str, commit_message: Optional[str] = None) -> Report:
        json = {"commit_message": commit_message}

        return Report.parse_obj(
            self.request("PATCH", f"/reports/{report}/sync_to_github", json=json)
        )
