# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a461390ea816d2e8db40e95d6a4296279b0e238cfb3c0374c7fcde1c34ae5874
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q019_private_release": """\
-- 共通の公開版と分離し、本人が編集する私有カタログを初回だけ用意する。
INSERT INTO recipeweave.catalog_release (id, version, manifest_hash, published_at, owner_id)
VALUES (%(release_id)s, %(version)s, %(manifest)s, NULL, %(user_id)s) ON CONFLICT (id) DO NOTHING;
""",
    "q020_custom_food": """\
-- 私有カタログへ本人の独自食材を登録する。
INSERT INTO recipeweave.food (id, code, name, kind, parent_id, release_id, status, owner_id)
VALUES (
    %(food_id)s, %(code)s, %(name)s, 'basic', NULL, %(release_id)s, 'active', %(user_id)s
) RETURNING id;
""",
    "q021_custom_owner": """\
-- 独自食材の所有者を認証主体へ固定する。
INSERT INTO recipeweave.user_food (id, user_id, food_id) VALUES (
    %(row_id)s, %(user_id)s, %(food_id)s
);
""",
    "q022_custom_form": """\
-- 独自食材にも標準形態と基準単位を用意する。
INSERT INTO recipeweave.food_form (id, food_id, name, state, base_unit_id, quantity_basis, status)
SELECT
    %(row_id)s AS id,
    %(food_id)s AS food_id,
    '標準' AS name,
    'raw' AS state,
    u.id AS base_unit_id,
    'as_purchased' AS quantity_basis,
    'active' AS status
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
    "q019_private_release": ("manifest", "release_id", "user_id", "version"),
    "q020_custom_food": ("code", "food_id", "name", "release_id", "user_id"),
    "q021_custom_owner": ("food_id", "row_id", "user_id"),
    "q022_custom_form": ("food_id", "row_id", "unit"),
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
