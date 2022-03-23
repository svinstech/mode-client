# mode-client

`mode-client` is a typed client for interaction with the [Mode API](https://mode.com/developer/api-reference/introduction/).

## Installation

`mode-client` requires Python version 3.7 or higher.

```shell
pip install mode-client
```

## Usage

```python
import mode_client

client = mode_client.ModeClient("workspace", "token", "password")
print(client.collection.list())
```

## Objects

The objects currently implemented are:

| Object                                                                           | Methods                                                                    |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| [`collection`](https://mode.com/developer/api-reference/management/collections/) | `get`, `list`, `create`, `update`, `delete`                                |
| [`report`](https://mode.com/developer/api-reference/analytics/reports/)          | `get`, `list`, `update`, `delete`, `archive`, `purge`, `unarchive`, `sync` |
| [`report_run`](https://mode.com/developer/api-reference/analytics/report-runs/)  | `get`, `list`, `clone`, `create`                                           |
| [`query`](https://mode.com/developer/api-reference/analytics/queries/)           | `get`, `list`, `create`, `update`, `delete`                                |
| [`query_run`](https://mode.com/developer/api-reference/analytics/query-runs/)    | `get`, `list`                                                              |

## FAQ

### What validation does `mode-client` perform?

`mode-client` uses [Pydantic](https://pydantic-docs.helpmanual.io) data types to validate the data returned from the Mode API.

### Why isn't `mode-client` asynchronous?

The Mode API throttles more than a single concurrent connection so the overhead of `async`/`await` isn't worth it.
