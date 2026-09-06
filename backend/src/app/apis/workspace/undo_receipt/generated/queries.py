# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 81a9ddebb79df36d3d42bc27df763fcbf01c29f96b81fca75177e5c3e135bea2
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_import": """-- 本人のレシート状態を確認して再取消を防ぐ。
SELECT
    id,
    status
FROM recipeweave.receipt_import
WHERE id = %(row_id)s AND user_id = %(user_id)s FOR UPDATE;
""",
    "q002_eligible_lots": """-- 消費・編集済み在庫を巻き戻さず、未使用の登録分だけを取り消す。
UPDATE recipeweave.pantry_lot AS p SET status = 'undone', updated_at = CURRENT_TIMESTAMP
WHERE
    p.source_import_id = %(row_id)s AND p.user_id = %(user_id)s AND NOT p.edited
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.pantry_consumption AS c
        WHERE c.lot_id = p.id
    )
RETURNING p.id;
""",
    "q003_revert": """-- 取消済みのレシートを再び登録状態へ戻さない。
UPDATE recipeweave.receipt_import SET
    status = 'reverted', reverted_at = CURRENT_TIMESTAMP, revision = revision + 1
WHERE id = %(row_id)s AND user_id = %(user_id)s AND status = 'committed' RETURNING id;
""",
    "q900_lock_revision": """-- 本人の集約版を排他ロックして並行操作の順序を確定する。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(user_id)s FOR UPDATE;
""",
    "q901_advance_revision": """-- 業務行の更新と同じトランザクションで版を一度だけ進める。
UPDATE recipeweave.workspace_revision SET revision = revision + 1
WHERE user_id = %(user_id)s RETURNING revision;
""",
    "q902_append_audit": """-- 個人データ本文を複製せず操作と対象キーのハッシュを記録する。
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
    "q001_import": ("row_id", "user_id"),
    "q002_eligible_lots": ("row_id", "user_id"),
    "q003_revert": ("row_id", "user_id"),
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
