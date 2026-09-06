# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 7c03c4ffbec4374e7c2b6fb317040181c3e3b08eea057b86940d70102fa34ade
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 保存直前に遅延FK・制約トリガーをすべて検証する。
SET CONSTRAINTS ALL IMMEDIATE;
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
