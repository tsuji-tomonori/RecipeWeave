# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    expected_etag: str
    name: str
    row_id: UUID
    unit_label: str


SQL = """-- 栄養成分種別を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.nutrient AS t
SET
    code = %(code)s,
    name = %(name)s,
    unit_label = %(unit_label)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.unit_label,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "expected_etag": values["expected_etag"],
        "name": values["name"],
        "row_id": values["row_id"],
        "unit_label": values["unit_label"],
    }
    return list(connection.execute(SQL, params).fetchall())
