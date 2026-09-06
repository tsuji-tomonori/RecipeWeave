# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    conditions: str
    expected_etag: str
    factor: Decimal
    form_id: UUID
    from_unit_id: UUID
    quality: str
    release_id: UUID
    row_id: UUID
    source_id: UUID | None
    to_unit_id: UUID


SQL = """-- 食材形態別換算を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.conversion AS t
SET
    form_id = %(form_id)s,
    from_unit_id = %(from_unit_id)s,
    to_unit_id = %(to_unit_id)s,
    factor = %(factor)s,
    quality = %(quality)s,
    source_id = %(source_id)s,
    conditions = %(conditions)s,
    release_id = %(release_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.form_id,
    t.from_unit_id,
    t.to_unit_id,
    t.factor,
    t.quality,
    t.source_id,
    t.conditions,
    t.release_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "conditions": values["conditions"],
        "expected_etag": values["expected_etag"],
        "factor": values["factor"],
        "form_id": values["form_id"],
        "from_unit_id": values["from_unit_id"],
        "quality": values["quality"],
        "release_id": values["release_id"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
        "to_unit_id": values["to_unit_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
