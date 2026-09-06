-- 新規書込みより前に料理版の公開条件または既存の本人履歴を検査する。
SELECT t.id
FROM recipeweave.recipe_version AS t
INNER JOIN recipeweave.recipe AS recipe ON t.recipe_id = recipe.id
WHERE
    t.id = %(reference_id)s
    AND (
        (t.status = 'published' AND t.validation = 'passed' AND recipe.status = 'published')
        OR (%(preview)s AND t.status = 'draft' AND recipe.status = 'draft')
        OR EXISTS (
            SELECT 1 FROM recipeweave.menu_item AS history_item
            INNER JOIN recipeweave.menu AS history_menu ON history_item.menu_id = history_menu.id
            WHERE history_menu.user_id = %(actor_id)s AND history_item.recipe_version_id = t.id
        )
        OR EXISTS (
            SELECT 1 FROM recipeweave.user_recipe_event AS history_event
            WHERE history_event.user_id = %(actor_id)s AND history_event.recipe_version_id = t.id
        )
    );
