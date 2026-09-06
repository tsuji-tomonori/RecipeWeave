-- 消費する量の正本はクライアントの適用結果でなくDBの需要行とする。
SELECT
    t.id,
    t.form_id,
    t.product_version_id,
    t.unit_id,
    t.required_amount,
    fm.food_id,
    fm.name AS form,
    u.code AS unit
FROM recipeweave.ingredient_total AS t INNER JOIN recipeweave.food_form AS fm ON t.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON t.unit_id = u.id
WHERE t.session_id = %(session_id)s
ORDER BY t.id;
