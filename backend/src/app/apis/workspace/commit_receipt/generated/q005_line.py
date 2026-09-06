# app-docs による自動生成。直接編集しない。
# SQLのSHA256: af2eb8834b3b2b5aa4823da6cf94e87bd19100c288057e6bfb23af069c06353e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 利用者が選択した商品だけを、登録ロットと対応付けて残す。
INSERT INTO recipeweave.receipt_line (
    id, import_id, line_no, raw_name, form_id, amount, unit_id, decision, pantry_lot_id
)
VALUES (
    %(row_id)s,
    %(import_id)s,
    %(line_no)s,
    %(name)s,
    %(form_id)s,
    %(amount)s,
    %(unit_id)s,
    'accepted',
    %(lot_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("amount", "form_id", "import_id", "line_no", "lot_id", "name", "row_id", "unit_id")
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
