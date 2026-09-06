# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 8f1ee1cc2cbff0ec4917f68c36caf3c4bd250128dd33d1f136255c5555b40022
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
    "q003_duplicate": """\
-- 画像と購入品構成の重複を本人の履歴だけで検出する。
SELECT
    id,
    status
FROM recipeweave.receipt_import
WHERE
    user_id = %(user_id)s
    AND (id = %(import_id)s OR file_sha256 = %(hash)s OR idempotency_key LIKE %(signature)s)
ORDER BY created_at;
""",
    "q004_import": """\
-- 再送キーと登録時刻を一度だけ確定する。画像本文は保持しない。
INSERT INTO recipeweave.receipt_import (
    id, user_id, file_sha256, idempotency_key, status, committed_at
)
VALUES (%(import_id)s, %(user_id)s, %(hash)s, %(key)s, 'committed', CURRENT_TIMESTAMP);
""",
    "q005_line": """\
-- 利用者が選択した商品だけを、登録ロットと対応付けて残す。
INSERT INTO recipeweave.receipt_line (
    id, import_id, line_no, raw_name, form_id, amount, unit_id, decision, pantry_lot_id
)
VALUES (
    %(row_id)s,
    %(import_id)s,
    %(line_no)s,
    %(name)s,
    %(form_id)s,
    %(amount)s,
    %(unit_id)s,
    'accepted',
    %(lot_id)s
);
""",
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
    "q003_duplicate": ("hash", "import_id", "signature", "user_id"),
    "q004_import": ("hash", "import_id", "key", "user_id"),
    "q005_line": (
        "amount",
        "form_id",
        "import_id",
        "line_no",
        "lot_id",
        "name",
        "row_id",
        "unit_id",
    ),
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
