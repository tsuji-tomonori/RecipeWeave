# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    row_id: UUID


SQL = """-- 組み合わせ・公開ルールを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.version,
    t.severity,
    t.predicate,
    t.message,
    t.source_id,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.compatibility_rule AS t
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
