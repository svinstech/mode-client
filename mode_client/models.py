from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class Link(BaseModel):
    href: str
    templated: Optional[bool]


class Avatar(BaseModel):
    type: str


class Pagination(BaseModel):
    page: int
    per_page: int
    count: int
    total_pages: int
    total_count: int


class QueryLinks(BaseModel):
    self: Link
    report: Link
    report_runs: Link
    charts: Optional[Link]
    new_chart: Optional[Link]
    new_query_table: Optional[Link]
    query_tables: Optional[Link]
    query_runs: Link
    creator: Link


class QueryRunLinks(BaseModel):
    self: Link
    query: Link
    view: Optional[Link]
    result: Link
    result_web: Link
    query_web: Link
    report_run: Link
    report_run_web: Link
    executed_by: Link


class ReportLinks(BaseModel):
    self: Link
    web: Link
    web_edit: Optional[Link]
    web_external_url: Optional[Link]
    csv_export: Optional[Link]
    share: Optional[Link]
    web_report_runs: Optional[Link]
    account: Link
    report_run: Link
    star: Optional[Link]
    space: Optional[Link]
    space_links: Optional[Link]
    queries: Link
    report_runs: Link
    report_pins: Link
    report_filters: Optional[Link]
    report_schedules: Optional[Link]
    report_subscriptions: Optional[Link]
    python_visualizations: Optional[Link]
    embed_key: Optional[Link]
    last_run: Link
    last_successful_run: Link
    python_notebook: Optional[Link]
    perspective_email_subscription_memberships: Optional[Link]
    validate_email_subscriber: Optional[Link]
    creator: Optional[Link]
    report_theme: Optional[Link]
    last_successful_github_sync: Optional[Link]
    report_index_web: Optional[Link]


class ReportRunLinks(BaseModel):
    latest_successful_report_run_api_url: Optional[Link]
    self: Link
    content: Optional[Link]
    preview: Optional[Link]
    account: Link
    report_schedule: Optional[Link]
    executed_by: Optional[Link]
    share: Optional[Link]
    embed: Optional[Link]
    report: Optional[Link]
    clone: Optional[Link]
    query_runs: Optional[Link]
    python_cell_runs: Optional[Link]
    pdf_export: Optional[Link]
    web_clone: Optional[Link]
    web_external_url: Optional[Link]


class SpaceLinks(BaseModel):
    self: Link
    detail: Link
    space_report_pins: Optional[Link]
    web: Optional[Link]
    reports: Link
    creator: Link
    user_space_membership: Optional[Link]
    space_memberships: Optional[Link]
    preview_space_memberships: Optional[Link]
    search_space_permissions: Link
    viewed: Optional[Link]


class DefinitionLinks(BaseModel):
    self: Link
    creator: Link
    last_run: Link
    last_successful_github_sync: Link
    web_edit: Link


class AccountLinks(BaseModel):
    self: Link
    web: Link
    web_settings: Optional[Link]
    web_data_sources_settings: Optional[Link]
    web_settings_slack: Optional[Link]
    web_public_datasource_home: Link
    web_spaces: Optional[Link]
    web_groups: Link
    web_new_organization: Link
    web_membership_events: Optional[Link]
    web_member_sessions: Optional[Link]
    web_settings_themes: Optional[Link]
    web_trial_appointments: Optional[Link]
    data_sources: Optional[Link]
    data_source: Optional[Link]
    admins: Optional[Link]
    memberships: Optional[Link]
    all_memberships: Optional[Link]
    home_web: Link
    home_starred_web: Link
    home_explorations_web: Link
    home_reports_web: Optional[Link]
    home_search_web: Link
    home_discover_web: Optional[Link]
    select_data_sources_web: Optional[Link]
    data_source_connection_request_web: Optional[Link]
    new_invite_web: Link
    new_upload_web: Link
    billing_web: Optional[Link]
    public_data_sources: Optional[Link]
    organizations: Optional[Link]
    preference: Optional[Link]
    table: Optional[Link]
    report: Link
    reports: Link
    archived_reports: Link
    public_reports: Link
    drafts_reports: Link
    starred_reports: Link
    by_ids_reports: Link
    viewed_reports: Link
    starred_datasets: Optional[Link]
    by_ids_datasets: Optional[Link]
    viewed_datasets: Optional[Link]
    starred_base_reports: Optional[Link]
    by_ids_base_reports: Optional[Link]
    viewed_base_reports: Optional[Link]
    by_tokens_definitions: Optional[Link]
    bridges: Optional[Link]
    access_tokens: Optional[Link]
    new_report: Optional[Link]
    new_report_web: Optional[Link]
    validate_table: Optional[Link]
    report_views: Optional[Link]
    groups: Optional[Link]
    group: Optional[Link]
    everyone_group: Optional[Link]
    users_groups_with_data_source_entitlements: Optional[Link]
    spaces: Optional[Link]
    space: Optional[Link]
    custom_spaces: Optional[Link]
    move_to_spaces: Optional[Link]
    definitions: Optional[Link]
    definition: Optional[Link]
    color_palettes: Optional[Link]
    all_color_palettes: Link
    color_palette: Optional[Link]
    web_color_palettes_settings: Optional[Link]
    validate_space_name: Optional[Link]
    validate_definition_name: Optional[Link]
    slack_app: Optional[Link]
    default_categorical_palette: Optional[Link]
    default_sequential_palette: Optional[Link]
    default_divergent_palette: Optional[Link]
    trial_appointment: Optional[Link]
    member_session_timeout: Optional[Link]
    easy_identity_providers: Optional[Link]
    saml_identity_providers: Optional[Link]
    scim_token: Optional[Link]
    memberships_lite: Optional[Link]


class Query(BaseModel):
    id: str
    token: str
    raw_query: Optional[str]
    created_at: str
    updated_at: str
    name: str
    last_run_id: Optional[str]
    data_source_id: str
    explorations_count: int
    report_imports_count: int
    mapping_id: Optional[str]
    links: QueryLinks = Field(alias="_links")


class QueryRun(BaseModel):
    id: str
    token: str
    raw_source: Optional[str]
    statement_annotation: Optional[str]
    state: str
    created_at: str
    completed_at: Optional[str]
    data_source_id: str
    limit: str
    query_token: str
    query_name: str
    query_created_at: str
    parameters: Dict[str, Any]
    rendered_source: Optional[str]
    max_result_bytes: str
    help_url: Optional[str]
    error_code: Optional[str]
    error_type: Optional[str]
    error_message: Optional[str]
    links: QueryRunLinks = Field(alias="_links")


class Report(BaseModel):
    token: str
    id: int
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str
    published_at: Optional[str]
    edited_at: str
    theme_id: Optional[int]
    color_mappings: Optional[Dict[str, Any]]
    type: str
    last_successful_sync_at: Optional[str]
    last_saved_at: str
    archived: bool
    space_token: Optional[str]
    account_id: int
    account_username: str
    public: bool
    full_width: Optional[bool]
    manual_run_disabled: bool
    run_privately: bool
    drilldowns_enabled: bool
    layout: Optional[str]
    is_embedded: Optional[bool]
    is_signed: Optional[bool]
    shared: Optional[bool]
    expected_runtime: float
    last_successfully_run_at: str
    last_run_at: str
    web_preview_image: Optional[str]
    last_successful_run_token: str
    flamingo_signature: Optional[str]
    github_link: Optional[str]
    query_count: int
    max_query_count: int
    chart_count: Optional[int]
    runs_count: int
    schedules_count: Optional[int]
    query_preview: str
    view_count: int
    links: ReportLinks = Field(alias="_links")


class ReportRun(BaseModel):
    token: str
    state: Optional[
        Literal[
            "pending",
            "enqueued",
            "cancelled",
            "failed",
            "succeeded",
            "completed",
            "running_notebook",
        ]
    ]
    created_at: str
    updated_at: str
    completed_at: Optional[str]
    purge_started_at: Optional[str]
    purge_completed_at: Optional[str]
    python_state: Optional[
        Literal["none", "pending", "failed", "submitted", "succeeded", "skipped"]
    ]
    form_fields: Optional[List[Any]]
    flamingo_signature: Optional[str]
    flamingo_host: Optional[str]
    is_latest_report_run: Optional[bool]
    is_latest_successful_report_run: Optional[bool]
    report_has_failures_since_last_success: Optional[bool]
    links: Optional[ReportRunLinks] = Field(alias="_links")


class ReportRuns(BaseModel):
    pagination: Pagination
    report_runs: List[ReportRun]


class Space(BaseModel):
    token: str
    id: int
    space_type: str
    name: str
    description: Optional[str]
    state: str
    restricted: bool
    free_default: str
    viewable_: str = Field(..., alias="viewable?")
    viewed_: Optional[str] = Field(None, alias="viewed?")
    default_access_level: Optional[str]
    links: SpaceLinks = Field(alias="_links")


class Definition(BaseModel):
    token: str
    id: int
    name: str
    description: str
    source: str
    data_source_id: str
    created_at: str
    updated_at: str
    last_successful_sync_at: str
    last_saved_at: str
    github_link: Optional[str]
    links: DefinitionLinks = Field(alias="_links")


class Account(BaseModel):
    username: str
    name: str
    id: int
    token: str
    email: Optional[str]
    dataset_size_limit_mb: str
    query_run_size_limit_mb: str
    email_verified: Optional[bool]
    avatar: Avatar
    user: bool
    space_count: Optional[int]
    data_source_count: Optional[int]
    organizations_count: Optional[int]
    trial_state: Optional[Literal["pending", "active", "expired"]]
    membership_type: Optional[Literal["admin", "full"]]
    payment_method_confirmed: Optional[bool]
    private_definition_count: Optional[int]
    private_definition_limit: Union[Optional[int], Literal["unlimited"]]
    authorized_domains: Optional[List[str]]
    plan_code: Optional[Literal["standard", "plus", "free"]]
    admin_data_source_connections_only: Optional[bool]
    scim_enabled: Optional[str]
    created_at: str
    settings: Optional[Dict[str, Any]]
    links: AccountLinks = Field(alias="_links")
