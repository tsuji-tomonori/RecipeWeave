-- 現在の献立を固定した本人用IDで読む。
SELECT
    mi.id,
    rv.recipe_id,
    mi.servings,
    mi.recipe_version_id,
    m.revision
FROM recipeweave.menu AS m INNER JOIN recipeweave.menu_item AS mi ON m.id = mi.menu_id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
ORDER BY mi.position, mi.id;
