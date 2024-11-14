import os

import pytest
from dotenv import load_dotenv

from mode_client import ModeClient


@pytest.fixture
def report_id():
    return os.getenv("MODE_REPORT_ID")


@pytest.fixture
def space_id():
    return os.getenv("MODE_SPACE_ID")


@pytest.fixture
def query_id():
    return os.getenv("MODE_QUERY_ID")


@pytest.fixture
def client():
    load_dotenv()
    return ModeClient(
        os.getenv("MODE_WORKSPACE"), os.getenv("MODE_TOKEN"), os.getenv("MODE_PASSWORD")
    )


def test_account(client):
    account = client.account.get("mode_client")
    assert account.username == "mode_client"


def test_space_list(client):
    custom_spaces = client.space.list()
    assert set(s.space_type for s in custom_spaces) == {"custom"}
    assert {"🚧Data Staging"}.issubset(set(s.name for s in custom_spaces))

    all_spaces = client.space.list("all")
    assert set(s.space_type for s in all_spaces) == {"custom", "private"}
    assert {"🚧Data Staging", "Personal"}.issubset(set(s.name for s in all_spaces))


def test_space_get(client):
    spaces = client.space.list()
    assert len(spaces) > 0

    space = client.space.get(spaces[0].token)
    assert space.name
    assert space.id
    assert space.token
    assert space.links


def test_report_list_space(client, space_id, report_id):
    if not space_id:
        pytest.skip("MODE_SPACE_ID not found")

    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    reports = client.report.list(space=space_id)
    assert set(r.token for r in reports) == {report_id}


def test_report_get(client, space_id, report_id):
    if not space_id:
        pytest.skip("MODE_SPACE_ID not found")

    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    report = client.report.get(report_id)
    assert report.name
    assert report.description
    assert report.type
    assert report.account_username
    assert report.chart_count
    assert report.query_count
    assert report.links.creator.href


def test_report_archive(client, report_id):
    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    report = client.report.get(report_id)
    assert report.archived is False

    client.report.archive(report_id)
    report = client.report.get(report_id)
    assert report.archived is True

    client.report.unarchive(report_id)
    report = client.report.get(report_id)
    assert report.archived is False


def test_report_update(client, report_id):
    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    report = client.report.get(report_id)
    old_name = report.name

    updated_name = f"[TEST] {old_name}"
    report = client.report.update(report_id, name=updated_name)
    assert report.name == updated_name

    report = client.report.update(report_id, name=old_name)
    assert report.name == old_name


def test_report_run(client, report_id):
    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    report_runs = client.report_run.list(report_id)
    num_runs = report_runs.pagination.total_count
    assert num_runs > 0

    latest_run = report_runs.report_runs[0]
    assert latest_run.token == client.report_run.get(report_id, latest_run.token).token

    created_report = client.report_run.create(report_id, {})
    report_runs = client.report_run.list(report_id)
    assert created_report.token == report_runs.report_runs[0].token
    assert report_runs.pagination.total_count == num_runs + 1


def test_query_list(client, report_id):
    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    queries = client.query.list(report_id)
    for q in queries:
        assert q.name


def test_query_get(client, report_id, query_id):
    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    if not query_id:
        pytest.skip("MODE_QUERY_ID not found")

    query = client.query.get(report_id, query_id)
    assert query.name
    assert query.raw_query


def test_query_run(client, report_id):
    if not report_id:
        pytest.skip("MODE_REPORT_ID not found")

    latest_run = client.report_run.list(report_id).report_runs[0].token
    query_runs = client.query_run.list(report_id, latest_run)
    assert len(query_runs) > 0

    query_run = query_runs[0].token
    query_run_data = client.query_run.get(report_id, latest_run, query_run)

    assert query_run_data.token == query_run


def test_definition_list(client):
    definitions = client.definition.list()
    assert len(definitions) > 0

    for definition in definitions:
        assert definition.name
        assert definition.id
        assert definition.token
        assert definition.source
        assert definition.links


def test_definition_get(client):
    definitions = client.definition.list()
    assert len(definitions) > 0

    definition = client.definition.get(definitions[0].token)
    assert definition.name
    assert definition.id
    assert definition.token
    assert definition.source
    assert definition.links
