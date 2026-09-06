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
