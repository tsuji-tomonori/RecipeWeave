-- 使用量の結果は合計表と消費台帳から導出する。
SELECT
    total.id,
    fm.food_id,
    fm.name AS form,
    total.required_amount,
    total.actual_amount,
    total.consumption_outcome,
    u.code AS unit,
    COALESCE(SUM(c.amount), 0) AS consumed_amount,
    ARRAY_AGG(c.lot_id ORDER BY c.created_at, c.id) FILTER (WHERE c.id IS NOT NULL) AS lot_ids
FROM recipeweave.ingredient_total AS total
INNER JOIN recipeweave.food_form AS fm ON total.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON total.unit_id = u.id
LEFT JOIN recipeweave.pantry_lot AS p
    ON
        total.form_id = p.form_id AND total.unit_id = p.unit_id
        AND total.product_version_id IS NOT DISTINCT FROM p.product_version_id
LEFT JOIN recipeweave.pantry_consumption AS c ON p.id = c.lot_id AND total.session_id = c.session_id
WHERE total.session_id = %(session_id)s
GROUP BY total.id, fm.food_id, fm.name, u.code
ORDER BY total.id;
