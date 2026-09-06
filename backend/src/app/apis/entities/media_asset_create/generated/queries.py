# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    locale: str
    media_type: str
    operation_id: UUID
    parameter_contract: Jsonb
    row_id: UUID
    sha256: str
    source_id: UUID
    uri: str
    validation: str
    version: int


SQL = """-- 教育用動画等の版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.media_asset AS t (
    id,
    operation_id,
    media_type,
    uri,
    sha256,
    locale,
    version,
    parameter_contract,
    source_id,
    validation
)
VALUES (
    %(row_id)s,
    %(operation_id)s,
    %(media_type)s,
    %(uri)s,
    %(sha256)s,
    %(locale)s,
    %(version)s,
    %(parameter_contract)s,
    %(source_id)s,
    %(validation)s
)
RETURNING
    t.id,
    t.created_at,
    t.operation_id,
    t.media_type,
    t.uri,
    t.sha256,
    t.locale,
    t.version,
    t.parameter_contract,
    t.source_id,
    t.validation,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "locale": values["locale"],
        "media_type": values["media_type"],
        "operation_id": values["operation_id"],
        "parameter_contract": values["parameter_contract"],
        "row_id": values["row_id"],
        "sha256": values["sha256"],
        "source_id": values["source_id"],
        "uri": values["uri"],
        "validation": values["validation"],
        "version": values["version"],
    }
    return list(connection.execute(SQL, params).fetchall())
