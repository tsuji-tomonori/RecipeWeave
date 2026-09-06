# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 28d23c84df05d94f5d486b7c4387f941b57cf44432b5ab0e514fdaf80e714df2
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_current": """-- 本人の進行中セッションを確認する。
SELECT
    s.id,
    s.menu_id,
    s.status,
    s.current_task_index
FROM recipeweave.cooking_session AS s
INNER JOIN
    recipeweave.menu AS m
    ON s.menu_id = m.id
WHERE
    m.user_id = %(user_id)s
    AND s.status IN ('planned', 'cooking', 'paused')
ORDER BY s.created_at DESC;
""",
    "q002_tasks": """-- 進捗更新の対象は本人のセッションに属する既存工程だけにする。
SELECT
    t.id,
    t.menu_item_id,
    t.step_id,
    t.status,
    t.timer_started_at,
    t.timer_duration_s,
    t.planned_start_s,
    t.planned_end_s
FROM recipeweave.session_task AS t
INNER JOIN recipeweave.cooking_session AS s ON t.session_id = s.id
INNER JOIN recipeweave.menu AS m ON s.menu_id = m.id
WHERE t.session_id = %(session_id)s AND m.user_id = %(user_id)s
ORDER BY t.planned_start_s, t.id;
""",
    "q003_progress": """-- 完了済み工程の巻戻しをせず進行位置と状態を更新する。
UPDATE recipeweave.cooking_session SET status = %(status)s, current_task_index = %(index)s
WHERE
    id = %(session_id)s AND status IN ('cooking', 'paused')
    AND EXISTS (
        SELECT 1 FROM recipeweave.menu AS m
        WHERE m.id = cooking_session.menu_id AND m.user_id = %(user_id)s
    )
RETURNING id;
""",
    "q004_complete_task": """-- 確認した工程を完了にし、最初の開始・完了時刻を保持する。
UPDATE recipeweave.session_task SET
    status = 'completed',
    actual_start_at = COALESCE(actual_start_at, CURRENT_TIMESTAMP),
    actual_end_at = COALESCE(actual_end_at, CURRENT_TIMESTAMP)
WHERE id = %(row_id)s AND session_id = %(session_id)s;
""",
    "q005_timer": """-- 開始済みタイマーを再送でリセットしない。
UPDATE recipeweave.session_task SET
    timer_started_at = CURRENT_TIMESTAMP,
    timer_duration_s = planned_end_s - planned_start_s
WHERE id = %(row_id)s AND session_id = %(session_id)s AND timer_started_at IS NULL;
""",
    "q006_totals": """-- 消費する量の正本はクライアントの適用結果でなくDBの需要行とする。
SELECT
    t.id,
    t.form_id, t.product_version_id,
    t.unit_id,
    t.required_amount,
    fm.food_id,
    fm.name AS form,
    u.code AS unit
FROM recipeweave.ingredient_total AS t INNER JOIN recipeweave.food_form AS fm ON t.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON t.unit_id = u.id
WHERE t.session_id = %(session_id)s
ORDER BY t.id;
""",
    "q007_available": """-- 同じ形態・単位の確定数量だけを期限と登録順で消費候補にする。
SELECT
    id,
    amount
FROM recipeweave.pantry_lot
WHERE
    user_id = %(user_id)s AND form_id = %(form_id)s AND unit_id = %(unit_id)s
    AND product_version_id IS NOT DISTINCT FROM %(product_id)s
AND status = 'active' AND quantity_quality = 'known' AND amount > 0
ORDER BY expires_on NULLS LAST, created_at, id FOR UPDATE;
""",
    "q008_consume": """-- 在庫の減算と台帳の追記は同じ要求トランザクションで確定する。
UPDATE recipeweave.pantry_lot SET amount = amount - %(amount)s, updated_at = CURRENT_TIMESTAMP
WHERE id = %(lot_id)s AND user_id = %(user_id)s AND amount >= %(amount)s RETURNING id;
""",
    "q009_ledger": """-- 同一セッションとロットの二重消費を一意制約で防ぐ。
INSERT INTO recipeweave.pantry_consumption (id, user_id, session_id, lot_id, amount, unit_id)
VALUES (%(row_id)s, %(user_id)s, %(session_id)s, %(lot_id)s, %(amount)s, %(unit_id)s);
""",
    "q010_outcome": """-- 計画量を上書きせず、実際に確認した使用量と適用結果を保存する。
UPDATE recipeweave.ingredient_total SET
    actual_amount = %(amount)s, consumption_outcome = %(outcome)s
WHERE id = %(total_id)s AND session_id = %(session_id)s;
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
    "q001_current": ("user_id",),
    "q002_tasks": ("session_id", "user_id"),
    "q003_progress": ("index", "session_id", "status", "user_id"),
    "q004_complete_task": ("row_id", "session_id"),
    "q005_timer": ("row_id", "session_id"),
    "q006_totals": ("session_id",),
    "q007_available": ("form_id", "product_id", "unit_id", "user_id"),
    "q008_consume": ("amount", "lot_id", "user_id"),
    "q009_ledger": ("amount", "lot_id", "row_id", "session_id", "unit_id", "user_id"),
    "q010_outcome": ("amount", "outcome", "session_id", "total_id"),
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
