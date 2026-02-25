import os
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementParameterListItem

_client = None


def _get_client() -> WorkspaceClient:
    global _client
    if _client is None:
        _client = WorkspaceClient()
    return _client


def execute(statement: str, parameters: list = None) -> list[dict]:
    """
    Execute a SQL statement and return rows as list of dicts.
    parameters: list of values, substituted positionally using ? placeholders.
    Internally converts ? to :p1, :p2, ... for the Databricks named-parameter API.
    """
    w = _get_client()
    wh_id = os.environ.get("DATABRICKS_WAREHOUSE_ID", "eaa098820703bf5f")

    # Databricks Statement Execution API requires named params (:p1, :p2, ...).
    # Replace each ? placeholder with the corresponding :pN token.
    if parameters:
        for i in range(len(parameters)):
            statement = statement.replace("?", f":p{i + 1}", 1)

    kwargs = dict(
        warehouse_id=wh_id,
        statement=statement,
        wait_timeout="30s",
    )
    if parameters:
        kwargs["parameters"] = [
            StatementParameterListItem(name=f"p{i + 1}", value=str(p))
            for i, p in enumerate(parameters)
        ]

    result = w.statement_execution.execute_statement(**kwargs)
    if result.status.error:
        raise RuntimeError(result.status.error.message)

    schema = result.manifest.schema if result.manifest else None
    cols = [c.name for c in (schema.columns if schema else [])]
    data = result.result.data_array if result.result else []
    rows = []
    for row in (data or []):
        rows.append(dict(zip(cols, row)))
    return rows


def query_one(statement: str, parameters: list = None) -> dict | None:
    """Execute a statement and return the first row, or None."""
    rows = execute(statement, parameters)
    return rows[0] if rows else None


def escape(s: str) -> str:
    """Escape single quotes for inline SQL string literals."""
    return s.replace("'", "''")
