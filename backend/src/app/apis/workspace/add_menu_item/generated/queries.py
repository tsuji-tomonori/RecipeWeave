# app-docs による自動生成。直接編集しない。
# SQLのSHA256: e6594513508df7f6c10d2bdcc1176465617b06934b7b30ccadc39bd210ed461d
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
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
    "q010_recipe": ("preview", "recipe_id", "requested_version_id"),
    "q011_ingredients": ("version_id",),
    "q012_menu": ("menu_id", "name", "user_id"),
    "q013_insert_item": ("menu_id", "role_option_id", "row_id", "servings", "version_id"),
    "q014_override": ("amount", "ingredient_id", "item_id", "row_id", "selected"),
    "q015_advance_menu": ("menu_id", "user_id"),
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
