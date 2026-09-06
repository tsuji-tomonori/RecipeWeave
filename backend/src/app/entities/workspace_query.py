# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    row_id: UUID


SQL = """-- 本人の変更を端末間の競合判定に反映し、業務更新と同時に版を増やす。
INSERT INTO recipeweave.workspace_revision AS current_revision (
    id, user_id, revision
)
VALUES (
    %(row_id)s, %(actor_id)s, 1
)
ON CONFLICT (user_id)
DO UPDATE SET revision = current_revision.revision + 1
RETURNING revision;
"""


def increment_workspace(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"actor_id": values["actor_id"], "row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
