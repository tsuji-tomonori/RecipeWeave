-- 献立の料理を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.menu_item AS t (
    id,
    menu_id,
    recipe_version_id,
    servings,
    role_option_id,
    position
)
VALUES (
    %(row_id)s,
    %(menu_id)s,
    %(recipe_version_id)s,
    %(servings)s,
    %(role_option_id)s,
    %(position)s
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
