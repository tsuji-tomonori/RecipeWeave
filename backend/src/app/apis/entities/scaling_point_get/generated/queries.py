# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    row_id: UUID


SQL = """-- 検証済み換算点を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.rule_id,
    t.servings,
    t.multiplier,
    t.xmin::TEXT AS etag
FROM recipeweave.scaling_point AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
