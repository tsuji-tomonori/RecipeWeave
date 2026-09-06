# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 1b3eb8165b3fabe8ecf74837ebb081645cf3bdb53c993ec863a9582d35594484
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_delete_item": """\
-- 本人の現在の献立の料理を外す。調理中の入力は専用の献立版へ保存する。
DELETE FROM recipeweave.menu_item
WHERE
    id = %(row_id)s AND menu_id = %(menu_id)s
    AND EXISTS (
        SELECT 1 FROM recipeweave.menu AS m
        WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
    )
RETURNING id;
""",
    "q900_lock_revision": """\
-- 本人の集約版を排他ロックして並行操作の順序を確定する。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(user_id)s FOR UPDATE;
""",
    "q901_advance_revision": """\
-- 業務行の更新と同じトランザクションで版を一度だけ進める。
UPDATE recipeweave.workspace_revision SET revision = revision + 1
WHERE user_id = %(user_id)s RETURNING revision;
""",
    "q902_append_audit": """\
-- 個人データ本文を複製せず操作と対象キーのハッシュを記録する。
INSERT INTO recipeweave.audit_event (
    id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at
)
VALUES (
    %(row_id)s, %(user_id)s, %(action)s, 'workspace', %(key_hash)s,
    '本人の業務操作', CURRENT_TIMESTAMP
);
""",
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "q001_delete_item": ("menu_id", "row_id", "user_id"),
    "q900_lock_revision": ("user_id",),
    "q901_advance_revision": ("user_id",),
    "q902_append_audit": ("action", "key_hash", "row_id", "user_id"),
}


def execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []
