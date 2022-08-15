import os
import time

import pytest
from dotenv import load_dotenv

from mode_client import ModeClient


@pytest.fixture(autouse=True)
def throttle():
    time.sleep(3)


@pytest.fixture
def report_id():
    return "8772ad79bc3f"


@pytest.fixture
def space_id():
    return "9764afb6d669"


@pytest.fixture
def query_id():
    return "f864867b8c7c"


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
    assert set(s.name for s in custom_spaces) == {"Mode Client"}

    all_spaces = client.space.list("all")
    assert set(s.space_type for s in all_spaces) == {"private", "custom"}
    assert set(s.name for s in all_spaces) == {"Mode Client", "Personal"}


def test_space_get(client):
    spaces = client.space.list()
    space = client.space.get(spaces[0].token)
    assert space.name == "Mode Client"


def test_report_list_space(client, space_id, report_id):
    reports = client.report.list(space=space_id)
    assert set(r.token for r in reports) == {report_id}


def test_report_get(client, report_id):
    report = client.report.get(report_id)
    assert report.name == "Dunder Mifflin"
    assert report.description == "A dashboard showing Dunder Mifflin sales"
    assert report.type == "Report"
    assert report.account_username == "mode_client"
    assert report.chart_count == 2
    assert report.query_count == 1
    assert report.archived is False
    assert report.links.creator.href == "/api/kshitij_aranke"


def test_report_archive(client, report_id):
    report = client.report.get(report_id)
    assert report.archived is False

    client.report.archive(report_id)
    report = client.report.get(report_id)
    assert report.archived is True

    client.report.unarchive(report_id)
    report = client.report.get(report_id)
    assert report.archived is False


def test_report_update(client, report_id):
    report = client.report.get(report_id)
    assert report.name == "Dunder Mifflin"

    report = client.report.update(report_id, name="Jaffle Shop")
    assert report.name == "Jaffle Shop"

    report = client.report.update(report_id, name="Dunder Mifflin")
    assert report.name == "Dunder Mifflin"


def test_report_run(client, report_id):
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
    queries = client.query.list(report_id)
    assert set(q.name for q in queries) == {"Query 1", "Query 2"}


def test_query_get(client, report_id, query_id):
    query = client.query.get(report_id, query_id)
    assert query.name == "Query 1"
    assert query.raw_query.startswith("-- Returns first 100 rows")


def test_query_create(client, report_id):
    client.query.create(
        report_id, "SELECT * FROM tutorial.flights limit 100;", 1, "flights"
    )

    queries = client.query.list(report_id)
    assert set(q.name for q in queries) == {"Query 1", "Query 2", "flights"}

    query = [q for q in queries if q.name == "flights"][0]
    assert query.raw_query == "SELECT * FROM tutorial.flights limit 100;"
    assert query.name == "flights"

    query = client.query.update(
        report_id,
        query.token,
        raw_query="SELECT * FROM tutorial.flights limit 10;",
        name="flights2",
    )
    assert query.raw_query == "SELECT * FROM tutorial.flights limit 10;"
    assert query.name == "flights2"

    client.query.delete(report_id, query.token)
    queries = client.query.list(report_id)
    assert set(q.name for q in queries) == {"Query 1", "Query 2"}


def test_query_run(client, report_id):
    latest_run = client.report_run.list(report_id).report_runs[0].token
    query_runs = client.query_run.list(report_id, latest_run)
    assert len(query_runs) > 0

    query_run = query_runs[0].token
    query_run_data = client.query_run.get(report_id, latest_run, query_run)

    assert query_run_data.token == query_run
