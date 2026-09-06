# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 70780a34840e7dbc4e6afc9027ab53853b36bee1202ebb5e9e9a7f9c3e6e320a
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの献立材料集計結果を元IDと全列で復元する。
INSERT INTO recipeweave.ingredient_total (
    id,
    created_at,
    session_id,
    form_id,
    product_version_id,
    unit_id,
    required_amount,
    quality,
    calculation_version,
    actual_amount,
    consumption_outcome
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(form_id)s,
    %(product_version_id)s,
    %(unit_id)s,
    %(required_amount)s,
    %(quality)s,
    %(calculation_version)s,
    %(actual_amount)s,
    %(consumption_outcome)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "actual_amount",
        "calculation_version",
        "consumption_outcome",
        "created_at",
        "form_id",
        "id",
        "product_version_id",
        "quality",
        "required_amount",
        "session_id",
        "unit_id",
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
