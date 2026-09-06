# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d56cfd46ecf5572a4fd090dfeabd09bd4753f5dd5334830b0fa96cb2462cfc7d
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_resolve_form": """\
-- 食材形態と単位をDBから検証し、他人の独自食材は参照させない。
SELECT
    fm.id AS form_id,
    u.id AS unit_id
FROM recipeweave.food_form AS fm
INNER JOIN recipeweave.food AS f ON fm.food_id = f.id
CROSS JOIN recipeweave.unit AS u
WHERE
    fm.food_id = %(food_id)s AND fm.name = %(form)s AND fm.status = 'active'
    AND u.code = %(unit)s AND u.status = 'active'
    AND (
        NOT EXISTS (
            SELECT 1 FROM recipeweave.user_food AS own
            WHERE own.food_id = f.id
        )
        OR EXISTS (
            SELECT 1 FROM recipeweave.user_food AS own
            WHERE own.food_id = f.id AND own.user_id = %(user_id)s
        )
    )
ORDER BY fm.id LIMIT 1;
""",
    "q002_insert_lot": """\
-- 登録時の値と現在値を一緒に記録する。不明数量はNULLのまま保持する。
INSERT INTO recipeweave.pantry_lot
(
    id, user_id, form_id, amount, unit_id, expires_on, location, priority, source_import_id,
    quantity_quality, original_form_id, original_amount, original_unit_id
)
VALUES (
    %(row_id)s, %(user_id)s, %(form_id)s, %(amount)s, %(unit_id)s, %(expires_on)s,
    %(location)s, %(priority)s, %(import_id)s, %(quality)s, %(form_id)s, %(amount)s, %(unit_id)s
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
    "q001_resolve_form": ("food_id", "form", "unit", "user_id"),
    "q002_insert_lot": (
        "amount",
        "expires_on",
        "form_id",
        "import_id",
        "location",
        "priority",
        "quality",
        "row_id",
        "unit_id",
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
