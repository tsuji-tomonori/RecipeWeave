-- 検証済みバックアップの献立の料理を元IDと全列で復元する。
INSERT INTO recipeweave.menu_item (
    id,
    created_at,
    menu_id,
    recipe_version_id,
    servings,
    role_option_id,
    position
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_id)s,
    %(recipe_version_id)s,
    %(servings)s,
    %(role_option_id)s,
    %(position)s
);
