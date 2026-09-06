# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    after_id: UUID | None
    page_limit: int


SQL = """-- レシピ材料明細を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.line_no,
    t.form_id,
    t.product_version_id,
    t.component_id,
    t.kit_parent_line_id,
    t.role,
    t.demand_kind,
    t.amount_mode,
    t.amount,
    t.amount_max,
    t.unit_id,
    t.canonical_amount,
    t.conversion_id,
    t.scaling_rule_id,
    t.optional,
    t.note,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_ingredient AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"after_id": values["after_id"], "page_limit": values["page_limit"]}
    return list(connection.execute(SQL, params).fetchall())
