# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    action: str
    actor_id: UUID
    entity_key_hash: str
    entity_type: str
    row_id: UUID


SQL = """-- 個人本文を複製せず、同じ業務トランザクションで変更履歴を追記する。
INSERT INTO recipeweave.audit_event (
    id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at
)
VALUES (
    %(row_id)s, %(actor_id)s, %(action)s, %(entity_type)s,
    %(entity_key_hash)s, 'APIによる正規化データ操作', NOW()
)
RETURNING id;
"""


def append_audit(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "action": values["action"],
        "actor_id": values["actor_id"],
        "entity_key_hash": values["entity_key_hash"],
        "entity_type": values["entity_type"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
