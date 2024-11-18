import unittest
from unittest.mock import patch, MagicMock
from mode_client.clients import (
    ModeBaseClient,
    ModeAccountClient,
    ModeQueryClient,
    ModeReportClient,
    ModeQueryRunClient,
    ModeSpaceClient,
    ModeDefinitionClient,
    ModeReportRunClient,
)


class TestModeAccountClient(unittest.TestCase):
    @patch.object(ModeBaseClient, "request")
    def test_get_account(self, mock_request):
        mock_request.return_value = {"id": "123", "username": "test user"}
        client = ModeAccountClient("workspace", "token", "password")

        with patch("mode_client.models.Account.parse_obj") as mock_parse_obj:
            mock_account = MagicMock()
            mock_parse_obj.return_value = mock_account
            account = client.get("123")
            self.assertEqual(account, mock_account)
            mock_request.assert_called_once_with("GET", "/123")
            mock_parse_obj.assert_called_once_with(
                {"id": "123", "username": "test user"}
            )


class TestModeQueryClient(unittest.TestCase):
    @patch.object(ModeBaseClient, "request")
    def test_get_query(self, mock_request):
        mock_request.return_value = {"id": "query_id", "name": "test query"}
        client = ModeQueryClient("workspace", "token", "password")

        with patch("mode_client.models.Query.parse_obj") as mock_parse_obj:
            mock_query = MagicMock()
            mock_parse_obj.return_value = mock_query
            query = client.get("report_id", "query_id")
            self.assertEqual(query, mock_query)
            mock_request.assert_called_once_with(
                "GET", "/reports/report_id/queries/query_id"
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "query_id", "name": "test query"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_list_queries(self, mock_request):
        mock_request.return_value = {
            "_embedded": {
                "queries": [
                    {"id": "1", "name": "Query 1"},
                    {"id": "2", "name": "Query 2"},
                ]
            }
        }
        client = ModeQueryClient("workspace", "token", "password")

        with patch("mode_client.clients.parse_obj_as") as mock_parse_obj_as:
            mock_queries = [MagicMock(), MagicMock()]
            mock_parse_obj_as.return_value = mock_queries
            queries = client.list("report_id")
            self.assertEqual(queries, mock_queries)
            mock_request.assert_called_once_with("GET", "/reports/report_id/queries")
            mock_parse_obj_as.assert_called_once()

    @patch.object(ModeBaseClient, "request")
    def test_create_query(self, mock_request):
        client = ModeQueryClient("workspace", "token", "password")
        client.create("report_id", "SELECT * FROM table", 1, "New Query")
        mock_request.assert_called_once_with(
            "POST",
            "/reports/report_id/queries",
            json={
                "query": {
                    "raw_query": "SELECT * FROM table",
                    "data_source_id": 1,
                    "name": "New Query",
                }
            },
        )

    @patch.object(ModeBaseClient, "request")
    def test_update_query(self, mock_request):
        mock_request.return_value = {"id": "query_id", "name": "updated query"}
        client = ModeQueryClient("workspace", "token", "password")
        with patch("mode_client.models.Query.parse_obj") as mock_parse_obj:
            mock_query = MagicMock()
            mock_parse_obj.return_value = mock_query
            updated_query = client.update(
                "report_id",
                "query_id",
                "SELECT * FROM updated_table",
                2,
                "updated query",
            )
            self.assertEqual(updated_query, mock_query)
            mock_request.assert_called_once_with(
                "PATCH",
                "/reports/report_id/queries/query_id",
                json={
                    "query": {
                        "raw_query": "SELECT * FROM updated_table",
                        "data_source_id": 2,
                        "name": "updated query",
                    }
                },
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "query_id", "name": "updated query"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_delete_query(self, mock_request):
        client = ModeQueryClient("workspace", "token", "password")
        client.delete("report_id", "query_id")
        mock_request.assert_called_once_with(
            "DELETE", "/reports/report_id/queries/query_id"
        )


class TestModeQueryRunClient(unittest.TestCase):
    @patch.object(ModeBaseClient, "request")
    def test_get_query_run(self, mock_request):
        mock_request.return_value = {"id": "query_run_id", "status": "completed"}
        client = ModeQueryRunClient("workspace", "token", "password")
        with patch("mode_client.models.QueryRun.parse_obj") as mock_parse_obj:
            mock_query_run = MagicMock()
            mock_parse_obj.return_value = mock_query_run
            query_run = client.get("report_id", "run_id", "query_run_id")
            self.assertEqual(query_run, mock_query_run)
            mock_request.assert_called_once_with(
                "GET", "/reports/report_id/runs/run_id/query_runs/query_run_id"
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "query_run_id", "status": "completed"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_list_query_runs(self, mock_request):
        mock_request.return_value = {
            "_embedded": {
                "query_runs": [
                    {"id": "query_run1", "status": "running"},
                    {"id": "query_run2", "status": "completed"},
                ]
            }
        }
        client = ModeQueryRunClient("workspace", "token", "password")
        with patch("mode_client.clients.parse_obj_as") as mock_parse_obj_as:
            mock_query_runs = [MagicMock(), MagicMock()]
            mock_parse_obj_as.return_value = mock_query_runs
            query_runs = client.list("report_id", "run_id")
            self.assertEqual(query_runs, mock_query_runs)
            mock_request.assert_called_once_with(
                "GET", "/reports/report_id/runs/run_id/query_runs"
            )
            mock_parse_obj_as.assert_called_once()


class TestModeReportClient(unittest.TestCase):
    @patch.object(ModeBaseClient, "request")
    def test_get_report(self, mock_request):
        mock_request.return_value = {"id": "report_id", "name": "test report"}
        client = ModeReportClient("workspace", "token", "password")
        with patch("mode_client.models.Report.parse_obj") as mock_parse_obj:
            mock_report = MagicMock()
            mock_parse_obj.return_value = mock_report
            report = client.get("report_id")
            self.assertEqual(report, mock_report)
            mock_request.assert_called_once_with("GET", "/reports/report_id")
            mock_parse_obj.assert_called_once_with(
                {"id": "report_id", "name": "test report"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_list_reports(self, mock_request):
        mock_request.return_value = {
            "_embedded": {
                "reports": [
                    {"id": "report1", "name": "Report 1"},
                    {"id": "report2", "name": "Report 2"},
                ]
            }
        }
        client = ModeReportClient("workspace", "token", "password")
        with patch("mode_client.clients.parse_obj_as") as mock_parse_obj_as:
            mock_reports = [MagicMock(), MagicMock()]
            mock_parse_obj_as.return_value = mock_reports
            reports = client.list("space_token")
            self.assertEqual(reports, mock_reports)
            mock_request.assert_called_once_with(
                "GET",
                "/spaces/space_token/reports",
                params={"order": "desc", "order_by": "updated_at"},
            )
            mock_parse_obj_as.assert_called_once()

    @patch.object(ModeBaseClient, "request")
    def test_update_report(self, mock_request):
        mock_request.return_value = {"id": "report_id", "name": "updated report"}
        client = ModeReportClient("workspace", "token", "password")
        with patch("mode_client.models.Report.parse_obj") as mock_parse_obj:
            mock_report = MagicMock()
            mock_parse_obj.return_value = mock_report
            updated_report = client.update(
                "report_id", name="updated report", description="new description"
            )
            self.assertEqual(updated_report, mock_report)
            mock_request.assert_called_once_with(
                "PATCH",
                "/reports/report_id",
                json={
                    "report": {
                        "name": "updated report",
                        "description": "new description",
                    }
                },
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "report_id", "name": "updated report"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_delete_report(self, mock_request):
        client = ModeReportClient("workspace", "token", "password")
        client.delete("report_id")
        mock_request.assert_called_once_with("DELETE", "/reports/report_id")

    @patch.object(ModeBaseClient, "request")
    def test_archive_report(self, mock_request):
        mock_request.return_value = {"id": "report_id", "status": "archived"}
        client = ModeReportClient("workspace", "token", "password")
        with patch("mode_client.models.Report.parse_obj") as mock_parse_obj:
            mock_report = MagicMock()
            mock_parse_obj.return_value = mock_report
            archived_report = client.archive("report_id")
            self.assertEqual(archived_report, mock_report)
            mock_request.assert_called_once_with("PATCH", "/reports/report_id/archive")
            mock_parse_obj.assert_called_once_with(
                {"id": "report_id", "status": "archived"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_sync_report(self, mock_request):
        mock_request.return_value = {"id": "report_id", "status": "synced"}
        client = ModeReportClient("workspace", "token", "password")
        with patch("mode_client.models.Report.parse_obj") as mock_parse_obj:
            mock_report = MagicMock()
            mock_parse_obj.return_value = mock_report
            synced_report = client.sync("report_id", commit_message="sync to github")
            self.assertEqual(synced_report, mock_report)
            mock_request.assert_called_once_with(
                "PATCH",
                "/reports/report_id/sync_to_github",
                json={"commit_message": "sync to github"},
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "report_id", "status": "synced"}
            )


class TestModeReportRunClient(unittest.TestCase):
    @patch.object(ModeBaseClient, "request")
    def test_get_report_run(self, mock_request):
        mock_request.return_value = {"id": "run_id", "status": "running"}
        client = ModeReportRunClient("workspace", "token", "password")
        with patch("mode_client.models.ReportRun.parse_obj") as mock_parse_obj:
            mock_report_run = MagicMock()
            mock_parse_obj.return_value = mock_report_run
            report_run = client.get("report_id", "run_id")
            self.assertEqual(report_run, mock_report_run)
            mock_request.assert_called_once_with(
                "GET", "/reports/report_id/runs/run_id"
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "run_id", "status": "running"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_clone_report_run(self, mock_request):
        mock_request.return_value = {"id": "new_run_id", "status": "cloned"}
        client = ModeReportRunClient("workspace", "token", "password")
        with patch("mode_client.models.ReportRun.parse_obj") as mock_parse_obj:
            mock_report_run = MagicMock()
            mock_parse_obj.return_value = mock_report_run
            cloned_run = client.clone("report_id", "run_id")
            self.assertEqual(cloned_run, mock_report_run)
            mock_request.assert_called_once_with(
                "POST", "/reports/report_id/runs/run_id/clone"
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "new_run_id", "status": "cloned"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_create_report_run(self, mock_request):
        mock_request.return_value = {"id": "new_run_id", "status": "created"}
        client = ModeReportRunClient("workspace", "token", "password")
        with patch("mode_client.models.ReportRun.parse_obj") as mock_parse_obj:
            mock_report_run = MagicMock()
            mock_parse_obj.return_value = mock_report_run
            parameters = {"param1": "value1", "param2": "value2"}
            created_run = client.create("report_id", parameters)
            self.assertEqual(created_run, mock_report_run)
            mock_request.assert_called_once_with(
                "POST", "/reports/report_id/runs", json={"parameters": parameters}
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "new_run_id", "status": "created"}
            )


class TestModeSpaceClient(unittest.TestCase):
    @patch.object(ModeBaseClient, "request")
    def test_get_space(self, mock_request):
        mock_request.return_value = {"id": "space_id", "name": "test space"}
        client = ModeSpaceClient("workspace", "token", "password")
        with patch("mode_client.models.Space.parse_obj") as mock_parse_obj:
            mock_space = MagicMock()
            mock_parse_obj.return_value = mock_space
            space = client.get("space_id")
            self.assertEqual(space, mock_space)
            mock_request.assert_called_once_with("GET", "/spaces/space_id")
            mock_parse_obj.assert_called_once_with(
                {"id": "space_id", "name": "test space"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_list_spaces(self, mock_request):
        mock_request.return_value = {
            "_embedded": {
                "spaces": [
                    {"id": "space1", "name": "Space 1"},
                    {"id": "space2", "name": "Space 2"},
                ]
            }
        }
        client = ModeSpaceClient("workspace", "token", "password")
        with patch("mode_client.clients.parse_obj_as") as mock_parse_obj_as:
            mock_spaces = [MagicMock(), MagicMock()]
            mock_parse_obj_as.return_value = mock_spaces
            spaces = client.list(filter_="all")
            self.assertEqual(spaces, mock_spaces)
            mock_request.assert_called_once_with(
                "GET", "/spaces", params={"filter": "all"}
            )
            mock_parse_obj_as.assert_called_once()

    @patch.object(ModeBaseClient, "request")
    def test_create_space(self, mock_request):
        mock_request.return_value = {"id": "new_space_id", "name": "new space"}
        client = ModeSpaceClient("workspace", "token", "password")
        with patch("mode_client.models.Space.parse_obj") as mock_parse_obj:
            mock_space = MagicMock()
            mock_parse_obj.return_value = mock_space
            space = client.create("new space", "description for new space")
            self.assertEqual(space, mock_space)
            mock_request.assert_called_once_with(
                "POST",
                "/spaces",
                json={
                    "space": {
                        "name": "new space",
                        "description": "description for new space",
                    }
                },
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "new_space_id", "name": "new space"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_update_space(self, mock_request):
        mock_request.return_value = {"id": "space_id", "name": "updated space"}
        client = ModeSpaceClient("workspace", "token", "password")
        with patch("mode_client.models.Space.parse_obj") as mock_parse_obj:
            mock_space = MagicMock()
            mock_parse_obj.return_value = mock_space
            space = client.update(
                "space_id", name="updated space", description="updated description"
            )
            self.assertEqual(space, mock_space)
            mock_request.assert_called_once_with(
                "POST",
                "/spaces/space_id",
                json={
                    "space": {
                        "name": "updated space",
                        "description": "updated description",
                    }
                },
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "space_id", "name": "updated space"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_delete_space(self, mock_request):
        client = ModeSpaceClient("workspace", "token", "password")
        client.delete("space_id")
        mock_request.assert_called_once_with("DELETE", "/spaces/space_id")


class TestModeDefinitionClient(unittest.TestCase):
    @patch.object(ModeBaseClient, "request")
    def test_get_definition(self, mock_request):
        mock_request.return_value = {"id": "definition_id", "name": "test definition"}
        client = ModeDefinitionClient("workspace", "token", "password")
        with patch("mode_client.models.Definition.parse_obj") as mock_parse_obj:
            mock_definition = MagicMock()
            mock_parse_obj.return_value = mock_definition
            definition = client.get("definition_token")
            self.assertEqual(definition, mock_definition)
            mock_request.assert_called_once_with("GET", "/definitions/definition_token")
            mock_parse_obj.assert_called_once_with(
                {"id": "definition_id", "name": "test definition"}
            )

    @patch.object(ModeBaseClient, "request")
    def test_list_definitions(self, mock_request):
        mock_request.return_value = {
            "_embedded": {
                "definitions": [
                    {"id": "123", "name": "definition 1"},
                    {"id": "345", "name": "definition 2"},
                ]
            }
        }
        client = ModeDefinitionClient("workspace", "token", "password")
        with patch("mode_client.clients.parse_obj_as") as mock_parse_obj_as:
            mock_definitions = [MagicMock(), MagicMock()]
            mock_parse_obj_as.return_value = mock_definitions
            definitions = client.list(filter_="active", tokens=["token1", "token2"])
            self.assertEqual(definitions, mock_definitions)
            mock_request.assert_called_once_with(
                "GET",
                "/definitions",
                params={"filter": "active", "tokens": ["token1", "token2"]},
            )
            mock_parse_obj_as.assert_called_once()

    @patch.object(ModeBaseClient, "request")
    def test_sync_definition(self, mock_request):
        mock_request.return_value = {"id": "definition_id", "status": "synced"}
        client = ModeDefinitionClient("workspace", "token", "password")
        with patch("mode_client.models.Definition.parse_obj") as mock_parse_obj:
            mock_definition = MagicMock()
            mock_parse_obj.return_value = mock_definition
            definition = client.sync(
                "definition_token", commit_message="sync to github"
            )
            self.assertEqual(definition, mock_definition)
            mock_request.assert_called_once_with(
                "PATCH",
                "/definitions/definition_token/sync_to_github",
                json={"commit_message": "sync to github"},
            )
            mock_parse_obj.assert_called_once_with(
                {"id": "definition_id", "status": "synced"}
            )
