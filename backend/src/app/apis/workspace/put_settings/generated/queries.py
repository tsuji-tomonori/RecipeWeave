# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 496c9636cc2203f0fff54a3a298f57c9bb2d44e8919f0455ab1507fff9c27a6b
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_clear_exclusion": """\
-- 本人の設定だけを、同じトランザクション内で置き換える。
DELETE FROM recipeweave.user_exclusion
WHERE user_id = %(user_id)s;
""",
    "q002_clear_pantry": """\
-- 本人の設定だけを、同じトランザクション内で置き換える。
DELETE FROM recipeweave.user_pantry_food
WHERE user_id = %(user_id)s;
""",
    "q003_clear_equipment": """\
-- 予約履歴が参照する設備IDを保持し、画面で選択する器具だけを無効にする。
UPDATE recipeweave.kitchen_resource AS k SET active = FALSE
WHERE k.user_id = %(user_id)s AND EXISTS (
    SELECT 1 FROM recipeweave.resource_type AS r
    WHERE r.id = k.resource_type_id AND r.code NOT IN ('person', 'burner', 'bowl')
);
""",
    "q004_exclusion": """\
-- 除外する食品を明示して保存する。
INSERT INTO recipeweave.user_exclusion (id, user_id, food_id, allergen_id, strict)
VALUES (%(row_id)s, %(user_id)s, %(food_id)s, NULL, TRUE);
""",
    "q005_pantry": """\
-- 常備指定は食品ごとの関連行として保存する。
INSERT INTO recipeweave.user_pantry_food (id, user_id, food_id) VALUES (
    %(row_id)s, %(user_id)s, %(food_id)s
);
""",
    "q006_equipment": """\
-- 既存器具のID・容量・予約を保持して再有効化する。
UPDATE recipeweave.kitchen_resource AS kitchen
SET active = TRUE
FROM recipeweave.resource_type AS resource_kind
WHERE
    kitchen.user_id = %(user_id)s
    AND kitchen.resource_type_id = resource_kind.id
    AND resource_kind.name = %(name)s AND resource_kind.status = 'active'
RETURNING kitchen.id;
""",
    "q007_add_equipment": """\
-- 利用者の改訂行をロックした同一要求内で、未登録の器具だけを追加する。
INSERT INTO recipeweave.kitchen_resource (
    id, user_id, resource_type_id, name, capacity, quantity, active
)
SELECT
    %(row_id)s AS id,
    %(user_id)s AS user_id,
    resource_kind.id AS resource_type_id,
    resource_kind.name,
    NULL AS capacity,
    1 AS quantity,
    TRUE AS active
FROM recipeweave.resource_type AS resource_kind
WHERE
    resource_kind.name = %(name)s AND resource_kind.status = 'active'
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.kitchen_resource AS kitchen
        WHERE kitchen.user_id = %(user_id)s AND kitchen.resource_type_id = resource_kind.id
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
    "q001_clear_exclusion": ("user_id",),
    "q002_clear_pantry": ("user_id",),
    "q003_clear_equipment": ("user_id",),
    "q004_exclusion": ("food_id", "row_id", "user_id"),
    "q005_pantry": ("food_id", "row_id", "user_id"),
    "q006_equipment": ("name", "user_id"),
    "q007_add_equipment": ("name", "row_id", "user_id"),
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
