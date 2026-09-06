-- 献立の確定分量を材料行と上書き行から復元する。
SELECT
    mi.id AS menu_item_id,
    f.food_id,
    f.name AS form,
    ri.id AS ingredient_id,
    u.code AS unit,
    ov.id AS override_id,
    CASE WHEN ov.selected = FALSE THEN 0 ELSE ov.amount END AS override_amount,
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
