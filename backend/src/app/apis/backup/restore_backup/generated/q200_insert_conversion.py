# app-docs による自動生成。直接編集しない。
# SQLのSHA256: cc7e8e2dc6b4dccbdccde79df89ea34c4434a0c77d482155086a3a9445b29224
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの食材形態別換算を元IDと全列で復元する。
INSERT INTO recipeweave.conversion (
    id,
    created_at,
    form_id,
    from_unit_id,
    to_unit_id,
    factor,
    quality,
    source_id,
    conditions,
    release_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(from_unit_id)s,
    %(to_unit_id)s,
    %(factor)s,
    %(quality)s,
    %(source_id)s,
    %(conditions)s,
    %(release_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "conditions",
        "created_at",
        "factor",
        "form_id",
        "from_unit_id",
        "id",
        "quality",
        "release_id",
        "source_id",
        "to_unit_id",
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
