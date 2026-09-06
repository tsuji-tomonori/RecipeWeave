-- 独自食材にも標準形態と基準単位を用意する。
INSERT INTO recipeweave.food_form (id, food_id, name, state, base_unit_id, quantity_basis, status)
SELECT
    %(row_id)s AS id,
    %(food_id)s AS food_id,
    '標準' AS name,
    'raw' AS state,
    u.id AS base_unit_id,
    'as_purchased' AS quantity_basis,
    'active' AS status
FROM recipeweave.unit AS u
WHERE u.code = %(unit)s AND u.status = 'active' RETURNING id;
