# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 9104f0b82446fbb0b830442da123fe299bb914aefe55db8db7cf88b45c429af1
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_clear": """\
-- 現在の買い物確認を本人の範囲で置き換える。
DELETE FROM recipeweave.user_shopping_check
WHERE user_id = %(user_id)s;
""",
    "q002_insert": """\
-- 食品と単位を参照して、数量不明を含む購入確認を保存する。
INSERT INTO recipeweave.user_shopping_check (
    id, user_id, key, signature, food_id, amount, unit_id, checked_at, archived
)
SELECT
    %(row_id)s AS id,
    %(user_id)s AS user_id,
    %(key)s AS key,
    %(signature)s AS signature,
    %(food_id)s AS food_id,
    %(amount)s AS amount,
    u.id AS unit_id,
    %(checked_at)s AS checked_at,
    %(archived)s AS archived
FROM recipeweave.unit AS u
WHERE u.code = %(unit)s AND u.status = 'active' RETURNING id;
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
    "q001_clear": ("user_id",),
    "q002_insert": (
        "amount",
        "archived",
        "checked_at",
        "food_id",
        "key",
        "row_id",
        "signature",
        "unit",
        "user_id",
    ),
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
