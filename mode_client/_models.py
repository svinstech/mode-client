from __future__ import annotations

from typing import List, Dict, Literal, Union

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    per_page: int
    count: int
    total_pages: int
    total_count: int


class BatchQuery(BaseModel):
    id: int
    token: str
    name: str
    raw_query: str
    creator_email: str
    data_source_token: str
    report_id: int
    report_token: str
    space_id: int
    space_token: str


class BatchQueries(BaseModel):
    pagination: Pagination
    queries: List[BatchQuery]


class Report(BaseModel):
    token: str
    id: int
    name: str
    created_at: str
    updated_at: str
    edited_at: str
    theme_id: int
    color_mappings: Dict
    last_successful_sync_at: str
    last_saved_at: str
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
    last_successfully_run_at: str
    last_run_at: str
    web_preview_image: str
    last_successful_run_token: str
    query_count: str
    chart_count: str
    schedules_count: str
    query_preview: str
    description: str
    space_token: str
    flamingo_signature: str


class ReportRun(BaseModel):
    token: str
    state: Literal['pending', 'enqueued', 'cancelled', 'failed', 'succeeded', 'completed', 'running_notebook']
    parameters: Dict[str, Union[str, int]]
    created_at: str
    updated_at: str
    completed_at: str
    purge_started_at: str
    purge_completed_at: str
    python_state: Literal['none', 'pending', 'failed', 'submitted', 'succeeded']
    form_fields: List
