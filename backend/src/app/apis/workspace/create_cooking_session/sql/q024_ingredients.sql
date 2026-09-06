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
