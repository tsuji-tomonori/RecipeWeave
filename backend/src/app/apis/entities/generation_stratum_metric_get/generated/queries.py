# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    row_id: UUID


SQL = """-- 採用率・飽和度の実測を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.template_id,
    t.window_start,
    t.window_end,
    t.attempted,
    t.valid,
    t.unique_count,
    t.publishable,
    t.input_tokens,
    t.output_tokens,
    t.cost_amount,
    t.currency,
    t.stratum_key,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_stratum_metric AS t
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
