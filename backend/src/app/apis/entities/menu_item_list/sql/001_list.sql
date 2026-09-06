-- 献立の料理を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.menu_id,
    t.recipe_version_id,
    t.servings,
    t.role_option_id,
    t.position,
    t.xmin::TEXT AS etag
FROM recipeweave.menu_item AS t
WHERE
    EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    )
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
