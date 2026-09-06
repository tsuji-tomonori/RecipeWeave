# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 13f91518aa032c6bdba62bad5ff07dd7afbaf0081ff918f09d1f2acdae53c369
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "q001_steps": """\
-- 指定料理版の工程を要求の献立行IDへ対応させる。永続行は作成しない。
SELECT
    %(item_id)s::UUID AS item_id,
    %(position)s::INTEGER AS position,
    %(servings)s::NUMERIC AS servings,
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
FROM recipeweave.recipe_version AS rv
INNER JOIN recipeweave.recipe_step AS st ON rv.id = st.recipe_version_id
INNER JOIN recipeweave.scaling_rule AS sc ON st.scaling_rule_id = sc.id
WHERE rv.id = %(version_id)s
ORDER BY st.step_no;
""",
    "q002_dependencies": """\
-- 指定料理版の安全・材料・品質に基づく先行条件を読む。
SELECT
    %(item_id)s::UUID AS item_id,
    d.before_step_id,
    d.after_step_id,
    d.min_lag_s,
    d.max_lag_s,
    d.kind
FROM recipeweave.recipe_step AS st
INNER JOIN recipeweave.step_dependency AS d ON st.id = d.after_step_id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY d.id;
""",
    "q003_requirements": """\
-- 工程が必要とする器具の台数と単位容量を読む。
SELECT
    sr.step_id,
    sr.resource_type_id,
    sr.quantity,
    sr.capacity_min,
    sr.exclusive,
    rt.name,
    rt.code
FROM recipeweave.step_resource AS sr
INNER JOIN recipeweave.recipe_step AS st ON sr.step_id = st.id
INNER JOIN recipeweave.resource_type AS rt ON sr.resource_type_id = rt.id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY sr.step_id, rt.code;
""",
    "q004_resources": """\
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
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "q001_steps": ("item_id", "position", "servings", "version_id"),
    "q002_dependencies": ("item_id", "version_id"),
    "q003_requirements": ("version_id",),
    "q004_resources": ("user_id",),
}


def execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []
