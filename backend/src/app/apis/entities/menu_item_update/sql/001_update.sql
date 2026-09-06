-- 献立の料理を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.menu_item AS t
SET
    menu_id = %(menu_id)s,
    recipe_version_id = %(recipe_version_id)s,
    servings = %(servings)s,
    role_option_id = %(role_option_id)s,
    position = %(position)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    )
RETURNING
    t.id,
    t.created_at,
    t.menu_id,
    t.recipe_version_id,
    t.servings,
    t.role_option_id,
    t.position,
    t.xmin::TEXT AS etag;
