# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 38b5decf1176dc6834e9b184d78d3821da39cd8e9a7f7a9267315f736641994d
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップのレシートの商品候補と確定した在庫の対応を元IDと全列で復元する。
INSERT INTO recipeweave.receipt_line (
    id,
    created_at,
    import_id,
    line_no,
    raw_name,
    form_id,
    product_version_id,
    amount,
    unit_id,
    decision,
    pantry_lot_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(import_id)s,
    %(line_no)s,
    %(raw_name)s,
    %(form_id)s,
    %(product_version_id)s,
    %(amount)s,
    %(unit_id)s,
    %(decision)s,
    %(pantry_lot_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "created_at",
        "decision",
        "form_id",
        "id",
        "import_id",
        "line_no",
        "pantry_lot_id",
        "product_version_id",
        "raw_name",
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
