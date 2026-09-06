# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 14f3b992c02eced61448184d7ae6bbb669101137264c7cc1b9b0e8ef59b03a1a
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの食材アレルゲン知識を元IDと全列で復元する。
INSERT INTO recipeweave.food_allergen (
    id,
    created_at,
    form_id,
    allergen_id,
    presence,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("allergen_id", "created_at", "form_id", "id", "presence", "source_id")
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
