# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 7259c2c2e35b584f332510c5e5ba01dd637f349154bd064b20c8872b0150b9a1
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの調理計画実行を元IDと全列で復元する。
INSERT INTO recipeweave.cooking_session (
    id,
    created_at,
    menu_id,
    menu_revision,
    status,
    target_at,
    planner_version,
    input_snapshot,
    input_hash,
    current_task_index
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_id)s,
    %(menu_revision)s,
    %(status)s,
    %(target_at)s,
    %(planner_version)s,
    %(input_snapshot)s,
    %(input_hash)s,
    %(current_task_index)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "created_at",
        "current_task_index",
        "id",
        "input_hash",
        "input_snapshot",
        "menu_id",
        "menu_revision",
        "planner_version",
        "status",
        "target_at",
    )
}


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
