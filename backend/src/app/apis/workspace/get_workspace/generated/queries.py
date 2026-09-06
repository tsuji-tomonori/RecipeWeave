# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 8c3f26443c1aef1f43292394253c8b1c243e302720e6d8d715500275c77f777c
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_revision": """-- 複数表の読取り中に本人の業務更新が割り込まないよう共有ロックする。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(user_id)s FOR SHARE;
""",
    "q002_lots": """-- 在庫本体・登録時の値・食材形態・単位を別々の正規化行から復元する。
SELECT
    p.id,
    f.food_id,
    f.name AS form,
    p.amount,
    u.code AS unit,
    p.original_amount,
    p.location,
    p.priority,
    p.expires_on,
    p.created_at,
    p.updated_at,
    p.source_import_id,
    p.status,
    p.edited,
    COALESCE(ofm.food_id, f.food_id) AS original_food_id,
    COALESCE(ou.code, u.code) AS original_unit
FROM recipeweave.pantry_lot AS p
INNER JOIN recipeweave.food_form AS f ON p.form_id = f.id
INNER JOIN recipeweave.unit AS u ON p.unit_id = u.id
LEFT JOIN recipeweave.food_form AS ofm ON p.original_form_id = ofm.id
LEFT JOIN recipeweave.unit AS ou ON p.original_unit_id = ou.id
WHERE p.user_id = %(user_id)s
ORDER BY p.created_at, p.id;
""",
    "q003_consumption": """-- 二重消費を防ぐ台帳からロットごとの使用履歴を読む。
SELECT
    c.lot_id,
    c.amount,
    u.code AS unit,
    c.session_id
FROM recipeweave.pantry_consumption AS c INNER JOIN recipeweave.unit AS u ON c.unit_id = u.id
WHERE c.user_id = %(user_id)s
ORDER BY c.created_at, c.id;
""",
    "q004_receipts": """-- 画像本文を保存せず、重複検知と取消しに必要な履歴だけを読む。
SELECT
    r.id,
    r.file_sha256,
    r.idempotency_key,
    r.created_at,
    r.status,
    r.reverted_at
FROM
    recipeweave.receipt_import AS r
WHERE
    r.user_id = %(user_id)s
    AND r.status IN ('committed', 'reverted')
ORDER BY r.created_at, r.id;
""",
    "q005_menu": """-- 現在の献立を固定した本人用IDで読む。
SELECT
    mi.id,
    rv.recipe_id,
    mi.servings,
    mi.recipe_version_id,
    m.revision
FROM recipeweave.menu AS m INNER JOIN recipeweave.menu_item AS mi ON m.id = mi.menu_id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
ORDER BY mi.position, mi.id;
""",
    "q006_ingredients": """-- 献立の確定分量を材料行と上書き行から復元する。
SELECT
    mi.id AS menu_item_id,
    f.food_id,
    f.name AS form,
    ri.id AS ingredient_id,
    CASE WHEN ov.selected = FALSE THEN 0 ELSE ov.amount END AS override_amount,
    u.code AS unit,
    ov.id AS override_id,
    ri.amount * mi.servings / rv.base_servings AS scaled_amount
FROM recipeweave.menu_item AS mi INNER JOIN recipeweave.menu AS m ON mi.menu_id = m.id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe_ingredient AS ri ON rv.id = ri.recipe_version_id
INNER JOIN recipeweave.food_form AS f ON ri.form_id = f.id
INNER JOIN recipeweave.unit AS u ON ri.unit_id = u.id
LEFT JOIN
    recipeweave.menu_ingredient_override AS ov
    ON mi.id = ov.menu_item_id AND ri.id = ov.ingredient_line_id
WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
ORDER BY mi.position, ri.line_no;
""",
    "q007_saved": """-- 保存と解除の追記イベントから、料理ごとの現在状態を導出する。
SELECT ranked.recipe_id FROM (
    SELECT
        rv.recipe_id,
        ev.kind,
        ROW_NUMBER()
            OVER (
                PARTITION BY rv.recipe_id
                ORDER BY ev.occurred_at DESC, ev.created_at DESC, ev.id DESC
            )
            AS rank
    FROM recipeweave.user_recipe_event AS ev
    INNER JOIN recipeweave.recipe_version AS rv ON ev.recipe_version_id = rv.id
    WHERE ev.user_id = %(user_id)s AND ev.kind IN ('liked', 'disliked')
) AS ranked
WHERE ranked.rank = 1 AND ranked.kind = 'liked'
ORDER BY ranked.recipe_id;
""",
    "q008_settings": """-- 除外・常備・器具を各設定表から一覧化する。
SELECT
    'excluded' AS kind,
    food_id::TEXT AS value
FROM recipeweave.user_exclusion
WHERE user_id = %(user_id)s AND food_id IS NOT NULL
UNION ALL
SELECT
    'pantry',
    food_id::TEXT
FROM recipeweave.user_pantry_food
WHERE user_id = %(user_id)s
UNION ALL
SELECT
    'equipment',
    r.name
FROM recipeweave.kitchen_resource AS k
INNER JOIN recipeweave.resource_type AS r ON k.resource_type_id = r.id
WHERE k.user_id = %(user_id)s AND k.active AND r.code NOT IN ('person', 'burner', 'bowl');
""",
    "q009_custom_foods": """-- 本人の独自食材は所有表を経由して取得する。
SELECT
    f.id,
    f.name,
    u.code AS unit
FROM recipeweave.user_food AS owned
INNER JOIN recipeweave.food AS f ON owned.food_id = f.id
INNER JOIN recipeweave.food_form AS fm ON f.id = fm.food_id
INNER JOIN recipeweave.unit AS u ON fm.base_unit_id = u.id
WHERE owned.user_id = %(user_id)s
ORDER BY f.name, f.id;
""",
    "q010_shopping": """-- 調理開始前にも利用できる本人の買い物確認を読む。
SELECT
    c.key AS client_key,
    c.signature,
    c.food_id,
    c.amount,
    u.code AS unit,
    c.checked_at,
    c.archived
FROM recipeweave.user_shopping_check AS c INNER JOIN recipeweave.unit AS u ON c.unit_id = u.id
WHERE c.user_id = %(user_id)s
ORDER BY c.checked_at, c.id;
""",
    "q011_session": """-- 本人の直近の調理を読む。入力の料理はセッション専用献立に固定済み。
SELECT
    s.id,
    s.menu_id,
    s.status,
    s.current_task_index,
    s.input_snapshot
FROM recipeweave.cooking_session AS s INNER JOIN recipeweave.menu AS m ON s.menu_id = m.id
WHERE m.user_id = %(user_id)s AND s.status <> 'cancelled'
ORDER BY s.created_at DESC, s.id DESC
LIMIT 1;
""",
    "q012_tasks": """-- 調理工程とタイマーを正規化されたタスクから読む。
SELECT
    t.id,
    t.menu_item_id,
    t.step_id,
    t.planned_start_s,
    t.planned_end_s,
    t.status,
    t.timer_started_at,
    t.timer_duration_s,
    rv.recipe_id,
    r.title AS recipe_name,
    st.title,
    st.instruction,
    st.attention,
    st.duration_max_s
FROM recipeweave.session_task AS t INNER JOIN recipeweave.menu_item AS mi ON t.menu_item_id = mi.id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe AS r ON rv.recipe_id = r.id
INNER JOIN recipeweave.recipe_step AS st ON t.step_id = st.id
WHERE t.session_id = %(session_id)s
ORDER BY t.planned_start_s, mi.position, st.step_no, t.id;
""",
    "q013_task_resources": """-- タスクに必要な器具の表示名を読む。
SELECT
    t.id AS task_id,
    r.name
FROM recipeweave.session_task AS t
INNER JOIN recipeweave.step_resource AS sr ON t.step_id = sr.step_id
INNER JOIN recipeweave.resource_type AS r ON sr.resource_type_id = r.id
WHERE t.session_id = %(session_id)s AND r.code <> 'person'
ORDER BY t.id, r.name;
""",
    "q014_totals": """-- 使用量の結果は合計表と消費台帳から導出する。
SELECT
    total.id,
    fm.food_id,
    fm.name AS form,
    total.required_amount,
    total.actual_amount,
    total.consumption_outcome,
    u.code AS unit,
    COALESCE(SUM(c.amount), 0) AS consumed_amount,
    ARRAY_AGG(c.lot_id) FILTER (WHERE c.id IS NOT NULL) AS lot_ids
FROM recipeweave.ingredient_total AS total
INNER JOIN recipeweave.food_form AS fm ON total.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON total.unit_id = u.id
LEFT JOIN recipeweave.pantry_lot AS p ON total.form_id = p.form_id AND total.unit_id = p.unit_id
LEFT JOIN recipeweave.pantry_consumption AS c ON p.id = c.lot_id AND total.session_id = c.session_id
WHERE total.session_id = %(session_id)s
GROUP BY total.id, fm.food_id, fm.name, u.code
ORDER BY total.id;
""",
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "q001_revision": ("user_id",),
    "q002_lots": ("user_id",),
    "q003_consumption": ("user_id",),
    "q004_receipts": ("user_id",),
    "q005_menu": ("menu_id", "user_id"),
    "q006_ingredients": ("menu_id", "user_id"),
    "q007_saved": ("user_id",),
    "q008_settings": ("user_id",),
    "q009_custom_foods": ("user_id",),
    "q010_shopping": ("user_id",),
    "q011_session": ("user_id",),
    "q012_tasks": ("session_id",),
    "q013_task_resources": ("session_id",),
    "q014_totals": ("session_id",),
}


def execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []
