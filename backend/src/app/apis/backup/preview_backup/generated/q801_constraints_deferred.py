# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 92e4ce672420ff25733c0c7fa902dedb804a5b5353abc712d8fd96dba4b5a478
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 復元する依存行の挿入順を組み立てる間は遅延可能な制約を保留する。
SET CONSTRAINTS ALL DEFERRED;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ()}


def _execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []


SQL = QUERIES["query"]


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """固定した単文SQLを実行する。"""
    return _execute(connection, "query", values)
