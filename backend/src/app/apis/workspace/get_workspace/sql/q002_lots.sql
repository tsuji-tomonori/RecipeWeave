-- 在庫本体・登録時の値・食材形態・単位を別々の正規化行から復元する。
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
