# mode-client

*mode-client* is a typed Python client for the [Mode API](https://mode.com/developer/api-reference/introduction/).

---

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mode-client)
![PyPI](https://img.shields.io/pypi/v/mode-client)
![PyPI - License](https://img.shields.io/pypi/l/mode-client)

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/k-aranke/mode-client/Test)
![pre-commit.ci status](https://results.pre-commit.ci/badge/github/k-aranke/mode-client/main.svg)
![Codecov](https://img.shields.io/codecov/c/github/k-aranke/mode-client)

## Installation

*mode-client* requires Python version 3.8 or higher.

```shell
pip install mode-client
```

## Usage

```python
import mode_client

client = mode_client.ModeClient("workspace", "token", "password")
print(client.space.list())
```

## API

The following objects and methods are implemented:

| Object                                                                                        | Methods                                                                                                                                                                                                                                               |
|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [account](https://mode.com/developer/api-reference/management/users/)<br/>(user/organization) | get(account) -> Account                                                                                                                                                                                                                               |
| [space](https://mode.com/developer/api-reference/management/collections/)<br/>(collection)    | get(space) -> Space<br/>list([filter]) -> List[Space]<br/>create(name, description) -> Space<br/>update(space, [name], [description]) -> Space<br/>delete(space)                                                                                      |
| [report](https://mode.com/developer/api-reference/analytics/reports/)                         | get(report) -> Report<br/>list(space) -> List[Report]<br/>update(report, [name], [description], [space_token]) -> Report<br/>delete(report)<br/>archive(report) -> Report<br/>unarchive(report) -> Report<br/>sync(report, [commit_message) -> Report |
| [report_run](https://mode.com/developer/api-reference/analytics/report-runs/)                 | get(report, run) -> ReportRun<br/>list(report) -> ReportRuns<br/>clone(report, run) -> ReportRun<br/>create(report, parameters) -> ReportRun                                                                                                          |
| [query](https://mode.com/developer/api-reference/analytics/queries/)                          | get(report, query) -> Query<br/>list(report) -> List[Query]<br/>create(report, raw_query, data_source_id, name)<br/>update(report, query, [raw_query], [data_source_id], [name]) -> Query<br/>delete(report, query)                                   |
| [query_run](https://mode.com/developer/api-reference/analytics/query-runs/)                   | get(report, run, query_run) -> QueryRun<br/>list(report, run) -> List[QueryRun]                                                                                                                                                                       |

## FAQ

### How do I find my workspace, token and password?

Your Mode workspace is the first part of your Mode URL (https://app.mode.com/organizations/<workspace>).

To obtain a Mode token and password, follow the instructions [here](https://mode.com/developer/api-reference/authentication/).

### Does *mode-client* support the full Mode API?

No, *mode-client* supports a subset of the Mode API most commonly used for auditing Mode workspaces.
If you'd like to see an object or method supported, please file a [GitHub issue](https://github.com/k-aranke/mode-client/issues/new).

### I'm getting a 429 error. What do I do?

Mode throttles clients to ~1 request/second.
If you're running into this error use `time.sleep` to slow down your requests.

### Why doesn't *mode-client* support Python 3.7?

*mode-client* uses the [typing.Literal](https://docs.python.org/3/library/typing.html#typing.Literal) type which was introduced in Python 3.8.

### What does it mean for *mode-client* to be typed?

*mode-client* is typed to enable explicit discovery of the methods for each object and their type signatures in the API.
This enables editor autocompletion for both code and data in line with modern Python best practices.

The data returned from the Mode API is also validated using [Pydantic](https://pydantic-docs.helpmanual.io) to ensure it is typed correctly.

### Does *mode-client* support Mode's [Discovery API](https://mode.com/developer/discovery-api/introduction/)?

No, *mode-client* captures the Mode workspace state in real time.
Mode's Discovery API is updated once a day which means the workspace state is always somewhat stale.
