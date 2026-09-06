# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    batch_capacity: Decimal | None
    max_servings: Decimal
    min_servings: Decimal
    mode: str
    name: str
    round_increment: Decimal
    round_mode: str
    row_id: UUID
    source_id: UUID | None


SQL = """-- 人数変更規則を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.scaling_rule AS t (
    id,
    name,
    mode,
    min_servings,
    max_servings,
    batch_capacity,
    round_mode,
    round_increment,
    source_id
)
VALUES (
    %(row_id)s,
    %(name)s,
    %(mode)s,
    %(min_servings)s,
    %(max_servings)s,
    %(batch_capacity)s,
    %(round_mode)s,
    %(round_increment)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.name,
    t.mode,
    t.min_servings,
    t.max_servings,
    t.batch_capacity,
    t.round_mode,
    t.round_increment,
    t.source_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "batch_capacity": values["batch_capacity"],
        "max_servings": values["max_servings"],
        "min_servings": values["min_servings"],
        "mode": values["mode"],
        "name": values["name"],
        "round_increment": values["round_increment"],
        "round_mode": values["round_mode"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
