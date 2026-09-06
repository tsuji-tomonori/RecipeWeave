# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    multiplier: Decimal
    row_id: UUID
    rule_id: UUID
    servings: Decimal


SQL = """-- 検証済み換算点を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.scaling_point AS t (
    id,
    rule_id,
    servings,
    multiplier
)
VALUES (
    %(row_id)s,
    %(rule_id)s,
    %(servings)s,
    %(multiplier)s
)
RETURNING
    t.id,
    t.created_at,
    t.rule_id,
    t.servings,
    t.multiplier,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "multiplier": values["multiplier"],
        "row_id": values["row_id"],
        "rule_id": values["rule_id"],
        "servings": values["servings"],
    }
    return list(connection.execute(SQL, params).fetchall())
