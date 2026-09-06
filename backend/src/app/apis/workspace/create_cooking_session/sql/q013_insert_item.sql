-- 検証した料理版と人数を献立へ登録する。
INSERT INTO recipeweave.menu_item (
    id, menu_id, recipe_version_id, servings, role_option_id, position
)
VALUES (
    %(row_id)s, %(menu_id)s, %(version_id)s, %(servings)s, NULL,
    (
        SELECT COALESCE(MAX(mi.position), 0) + 1 FROM recipeweave.menu_item AS mi
        WHERE mi.menu_id = %(menu_id)s
    )
)
RETURNING id;
