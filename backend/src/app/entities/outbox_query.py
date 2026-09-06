# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    aggregate_id: str
    event_type: str
    row_id: UUID


SQL = """-- カタログ変更の配信要求を業務と同じトランザクションで追記する。
INSERT INTO recipeweave.outbox_event (
    id, event_type, aggregate_id, payload, attempt_count
)
VALUES (
    %(row_id)s, %(event_type)s, %(aggregate_id)s,
    JSONB_BUILD_OBJECT(
        'schema_version', 1,
        'event_id', %(row_id)s::TEXT,
        'aggregate_id', %(aggregate_id)s::TEXT,
        'version', 1
    ), 0
)
RETURNING id;
"""


def append_outbox(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "aggregate_id": values["aggregate_id"],
        "event_type": values["event_type"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
