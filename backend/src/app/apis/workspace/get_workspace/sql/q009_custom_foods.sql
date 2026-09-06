-- 本人の独自食材は所有表を経由して取得する。
SELECT
    f.id,
    f.name,
    u.code AS unit
FROM recipeweave.user_food AS uf
INNER JOIN recipeweave.food AS f ON uf.food_id = f.id
INNER JOIN recipeweave.food_form AS fm ON f.id = fm.food_id
INNER JOIN recipeweave.unit AS u ON fm.base_unit_id = u.id
WHERE uf.user_id = %(user_id)s
ORDER BY f.name, f.id;
