# mode-client

`mode-client` is an async and typed client for interaction with the [Mode API](https://mode.com/developer/api-reference/introduction/).

## Installation

`mode-client` requires Python version 3.7 or higher for `async`/`await` and `typing`.

```shell
pip install mode-client
```

## Usage

```python
import asyncio

from mode_client import ModeClient


async def main():
    async with ModeClient('workspace', 'token', 'password') as client:
        return await client.collection.list()

collections = asyncio.run(main())
print(collections)
```

## Objects

The objects currently implemented are:

| Object                                                                           | Methods                                                                                                |
|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| [`collection`](https://mode.com/developer/api-reference/management/collections/) | `get`, `list`, `create`, `update`, `delete`                                                            |
| [`report`](https://mode.com/developer/api-reference/analytics/reports/)          | `get`, `list_using_data_source`, `list_for_space`, `update`, `delete`, `archive`, `purge`, `unarchive` |
| [`report_run`](https://mode.com/developer/api-reference/analytics/report-runs/)  | `get`, `list`, `clone`, `create`                                                                       |
| [`query`](https://mode.com/developer/api-reference/analytics/queries/)           | `get`, `list`, `create`, `update`, `delete`                                                            |
| [`query_run`](https://mode.com/developer/api-reference/analytics/query-runs/)    | `get`, `list`                                                                                          |

If you'd like to see an object implemented, please [create a new Github issue](https://github.com/k-aranke/mode-client/issues/new).

## FAQ

### Why is `mode-client` async?

`mode-client` is async to allow fetching multiple objects in parallel (e.g. all reports in a given collection).
This is especially important for time-constrained environments like AWS Lambda.

### Can I run `mode-client` synchronously?

Not directly, but you can wrap your async function in `asyncio.run` as shown in the `Usage` section earlier.

### Why are `mode-client` objects typed?

`mode-client` is typed to validate data coming from the Mode API.
Typing objects also makes selecting attributes easier since they can be recognized from a list instead of recalled from memory. 

### I don't see a `_links` attribute in the types?

`_links` often duplicate information in the rest of the object and their presence makes it difficult to take in the object at a glance.
Therefore, `_links` have been excluded from `mode-client`, but [create a new Github issue](https://github.com/k-aranke/mode-client/issues/new) if you'd like to see them here.
