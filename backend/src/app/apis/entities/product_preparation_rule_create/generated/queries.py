# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    allowed: bool
    operation_id: UUID
    parameter_contract: Jsonb
    product_version_id: UUID
    row_id: UUID
    source_id: UUID
    use_original_container: bool


SQL = """-- 商品固有の調理条件を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product_preparation_rule AS t (
    id,
    product_version_id,
    operation_id,
    allowed,
    use_original_container,
    parameter_contract,
    source_id
)
VALUES (
    %(row_id)s,
    %(product_version_id)s,
    %(operation_id)s,
    %(allowed)s,
    %(use_original_container)s,
    %(parameter_contract)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.product_version_id,
    t.operation_id,
    t.allowed,
    t.use_original_container,
    t.parameter_contract,
    t.source_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "allowed": values["allowed"],
        "operation_id": values["operation_id"],
        "parameter_contract": values["parameter_contract"],
        "product_version_id": values["product_version_id"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
        "use_original_container": values["use_original_container"],
    }
    return list(connection.execute(SQL, params).fetchall())
