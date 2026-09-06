# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 61b2aa64e704cdac40a09e208e8d9804de75299a3faeaf9a5356695637f6b8d9
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_current": """\
-- 本人の進行中セッションを確認する。
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
    "q010_recipe": """\
-- 公開済み料理、または明示したローカル試用で利用できる料理版を選ぶ。
SELECT
    rv.id,
    rv.base_servings,
    ARRAY(
        SELECT ao.id FROM recipeweave.recipe_option AS ro
        INNER JOIN recipeweave.axis_option AS ao ON ro.option_id = ao.id
        INNER JOIN recipeweave.axis AS ax ON ao.axis_id = ax.id
        WHERE ro.recipe_version_id = rv.id AND ax.code = 'dish_role'
        ORDER BY ao.id
    ) AS role_option_ids
FROM recipeweave.recipe_version AS rv
INNER JOIN
    recipeweave.recipe AS r
    ON rv.recipe_id = r.id
WHERE
    r.id = %(recipe_id)s
    AND (%(requested_version_id)s::UUID IS NULL OR rv.id = %(requested_version_id)s)
    AND (
        (rv.status = 'published' AND rv.validation = 'passed' AND r.status = 'published')
        OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft')
    )
ORDER BY rv.version DESC
LIMIT 1;
""",
    "q011_ingredients": """\
-- 指定料理の材料ID・単位・基準量を照合する。
SELECT
    ri.id,
    fm.food_id,
    ri.amount,
    ri.optional,
    ri.unit_id,
    ri.form_id,
    u.code AS unit
FROM recipeweave.recipe_ingredient AS ri
INNER JOIN recipeweave.food_form AS fm ON ri.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON ri.unit_id = u.id
WHERE ri.recipe_version_id = %(version_id)s
ORDER BY ri.line_no;
""",
    "q012_menu": """\
-- 現在の献立を初回だけ作成し、所有者を固定する。
INSERT INTO recipeweave.menu (id, user_id, name, servings, revision)
VALUES (%(menu_id)s, %(user_id)s, %(name)s, 2, 1) ON CONFLICT (id) DO NOTHING;
""",
    "q013_insert_item": """\
-- 検証した料理版と人数を献立へ登録する。
INSERT INTO recipeweave.menu_item (
    id, menu_id, recipe_version_id, servings, role_option_id, position
)
VALUES (
    %(row_id)s, %(menu_id)s, %(version_id)s, %(servings)s, %(role_option_id)s,
    (
        SELECT COALESCE(MAX(mi.position), 0) + 1 FROM recipeweave.menu_item AS mi
        WHERE mi.menu_id = %(menu_id)s
    )
)
RETURNING id;
""",
    "q014_override": """\
-- 利用者が確認した確定分量だけを元の材料行へ結び付ける。
INSERT INTO recipeweave.menu_ingredient_override (
    id, menu_item_id, ingredient_line_id, selected, amount, form_id, product_version_id
)
VALUES (%(row_id)s, %(item_id)s, %(ingredient_id)s, %(selected)s, %(amount)s, NULL, NULL);
""",
    "q015_advance_menu": """\
-- 調理計画が参照する献立版を更新する。
UPDATE recipeweave.menu SET revision = revision + 1
WHERE id = %(menu_id)s AND user_id = %(user_id)s RETURNING revision;
""",
    "q020_steps": """\
-- 料理版の工程と加熱時間の換算規則を読む。
SELECT
    mi.id AS item_id,
    mi.position,
    mi.servings,
    rv.base_servings,
    rv.recipe_id,
    st.id AS step_id,
    st.step_no,
    st.duration_max_s,
    st.attention,
    sc.mode AS scaling_mode,
    sc.batch_capacity,
    GREATEST(sc.min_servings, (
        SELECT MAX(ingredient_rule.min_servings)
        FROM recipeweave.recipe_ingredient AS ingredient
        INNER JOIN recipeweave.scaling_rule AS ingredient_rule
            ON ingredient.scaling_rule_id = ingredient_rule.id
        WHERE ingredient.recipe_version_id = rv.id
    )) AS min_servings,
    LEAST(sc.max_servings, (
        SELECT MIN(ingredient_rule.max_servings)
        FROM recipeweave.recipe_ingredient AS ingredient
        INNER JOIN recipeweave.scaling_rule AS ingredient_rule
            ON ingredient.scaling_rule_id = ingredient_rule.id
        WHERE ingredient.recipe_version_id = rv.id
    )) AS max_servings
FROM recipeweave.menu_item AS mi
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe_step AS st ON rv.id = st.recipe_version_id
INNER JOIN recipeweave.scaling_rule AS sc ON st.scaling_rule_id = sc.id
WHERE mi.menu_id = %(menu_id)s
ORDER BY mi.position, st.step_no;
""",
    "q021_dependencies": """\
-- 同一料理版の材料・品質・安全上の先行条件を読む。
SELECT
    mi.id AS item_id,
    d.before_step_id,
    d.after_step_id,
    d.min_lag_s,
    d.max_lag_s,
    d.kind
FROM recipeweave.menu_item AS mi
INNER JOIN recipeweave.recipe_step AS st ON mi.recipe_version_id = st.recipe_version_id
INNER JOIN recipeweave.step_dependency AS d ON st.id = d.after_step_id
WHERE mi.menu_id = %(menu_id)s
ORDER BY mi.position, d.id;
""",
    "q022_requirements": """\
-- 工程が占有する器具数と最小容量を読む。
SELECT
    sr.step_id,
    sr.resource_type_id,
    sr.quantity,
    sr.capacity_min,
    sr.exclusive,
    rt.name,
    rt.code
FROM recipeweave.step_resource AS sr
INNER JOIN recipeweave.resource_type AS rt ON sr.resource_type_id = rt.id
WHERE
    EXISTS (
        SELECT 1 FROM recipeweave.recipe_step AS st INNER JOIN recipeweave.menu_item AS mi
            ON st.recipe_version_id = mi.recipe_version_id
        WHERE mi.menu_id = %(menu_id)s AND st.id = sr.step_id
    )
ORDER BY sr.step_id, rt.code;
""",
    "q023_resources": """\
-- 本人が登録した実際の設備数と容量を読む。
SELECT
    k.id,
    k.resource_type_id,
    k.name,
    k.quantity,
    k.capacity,
    rt.code
FROM recipeweave.kitchen_resource AS k
INNER JOIN recipeweave.resource_type AS rt ON k.resource_type_id = rt.id
WHERE k.user_id = %(user_id)s AND k.active
ORDER BY rt.code, k.id;
""",
    "q024_ingredients": """\
-- 分量を食品名でなく形態・単位・商品版ごとに合計する。
SELECT
    ri.id AS ingredient_id,
    ri.form_id,
    ri.product_version_id,
    ri.unit_id,
    ri.conversion_id,
    mi.id AS item_id,
    rv.id AS recipe_version_id,
    mi.servings,
    COALESCE(ov.amount, ri.amount * mi.servings / rv.base_servings) AS amount
FROM recipeweave.menu_item AS mi
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe_ingredient AS ri ON rv.id = ri.recipe_version_id
LEFT JOIN
    recipeweave.menu_ingredient_override AS ov
    ON mi.id = ov.menu_item_id AND ri.id = ov.ingredient_line_id
WHERE
    mi.menu_id = %(menu_id)s AND ri.demand_kind <> 'kit_component'
    AND (NOT ri.optional OR ov.selected)
ORDER BY mi.position, ri.line_no;
""",
    "q025_session": """\
-- 正規化した入力行の識別子・固定量だけを版付き入力契約へ保存する。
INSERT INTO recipeweave.cooking_session
(id, menu_id, menu_revision, status, target_at, planner_version, input_snapshot, input_hash)
VALUES (
    %(session_id)s,
    %(menu_id)s,
    %(revision)s,
    'cooking',
    NULL,
    'dag-resource-v1',
    %(snapshot)s,
    %(hash)s
);
""",
    "q026_task": """\
-- 計画済み工程を独立したタスク行へ保存する。
INSERT INTO recipeweave.session_task
(
    id, session_id, menu_item_id, step_id, batch_no, planned_start_s, planned_end_s, status,
    duration_source, confirmed_duration_s
)
VALUES (
    %(row_id)s, %(session_id)s, %(item_id)s, %(step_id)s, 1, %(start)s, %(end)s, 'pending',
    %(duration_source)s, %(confirmed_duration_s)s
);
""",
    "q027_dependency": """\
-- 工程の先行条件を具体的なタスク間に移す。
INSERT INTO recipeweave.task_dependency (
    id, before_task_id, after_task_id, min_lag_s, max_lag_s, reason
)
VALUES (%(row_id)s, %(before_id)s, %(after_id)s, %(min_lag)s, %(max_lag)s, %(reason)s);
""",
    "q028_reservation": """\
-- 本人の設備を必要な時間と数だけ予約する。
INSERT INTO recipeweave.resource_reservation (id, task_id, resource_id, start_s, end_s, quantity)
VALUES (%(row_id)s, %(task_id)s, %(resource_id)s, %(start)s, %(end)s, %(quantity)s);
""",
    "q029_total": """\
-- 同じ商品・形態・単位の確定需要を一つに合計する。
INSERT INTO recipeweave.ingredient_total
(
    id,
    session_id,
    form_id,
    product_version_id,
    unit_id,
    required_amount,
    quality,
    calculation_version
)
VALUES (
    %(row_id)s,
    %(session_id)s,
    %(form_id)s,
    %(product_id)s,
    %(unit_id)s,
    %(amount)s,
    'reference',
    'decimal-v1'
);
""",
    "q030_menu_revision": """\
-- 計画が参照する専用献立の確定版を読む。
SELECT revision FROM recipeweave.menu
WHERE id = %(menu_id)s AND user_id = %(user_id)s;
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
    "q001_current": ("user_id",),
    "q010_recipe": ("preview", "recipe_id", "requested_version_id"),
    "q011_ingredients": ("version_id",),
    "q012_menu": ("menu_id", "name", "user_id"),
    "q013_insert_item": ("menu_id", "role_option_id", "row_id", "servings", "version_id"),
    "q014_override": ("amount", "ingredient_id", "item_id", "row_id", "selected"),
    "q015_advance_menu": ("menu_id", "user_id"),
    "q020_steps": ("menu_id",),
    "q021_dependencies": ("menu_id",),
    "q022_requirements": ("menu_id",),
    "q023_resources": ("user_id",),
    "q024_ingredients": ("menu_id",),
    "q025_session": ("hash", "menu_id", "revision", "session_id", "snapshot"),
    "q026_task": (
        "confirmed_duration_s",
        "duration_source",
        "end",
        "item_id",
        "row_id",
        "session_id",
        "start",
        "step_id",
    ),
    "q027_dependency": ("after_id", "before_id", "max_lag", "min_lag", "reason", "row_id"),
    "q028_reservation": ("end", "quantity", "resource_id", "row_id", "start", "task_id"),
    "q029_total": ("amount", "form_id", "product_id", "row_id", "session_id", "unit_id"),
    "q030_menu_revision": ("menu_id", "user_id"),
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
