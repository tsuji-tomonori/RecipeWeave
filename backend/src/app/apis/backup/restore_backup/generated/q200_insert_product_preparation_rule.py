# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d6f4516420ae7edd3ca867bcaf69b6b291d0b3835a654cf4a36b67694efa3afb
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの商品固有の調理条件を元IDと全列で復元する。
INSERT INTO recipeweave.product_preparation_rule (
    id,
    created_at,
    product_version_id,
    operation_id,
    allowed,
    use_original_container,
    parameter_contract,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(operation_id)s,
    %(allowed)s,
    %(use_original_container)s,
    %(parameter_contract)s,
    %(source_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "allowed",
        "created_at",
        "id",
        "operation_id",
        "parameter_contract",
        "product_version_id",
        "source_id",
        "use_original_container",
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
