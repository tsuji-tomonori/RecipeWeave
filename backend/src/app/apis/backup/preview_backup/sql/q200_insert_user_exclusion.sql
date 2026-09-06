-- 検証済みバックアップの避けたい食材・物質を元IDと全列で復元する。
INSERT INTO recipeweave.user_exclusion (
    id,
    created_at,
    user_id,
    food_id,
    allergen_id,
    strict
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(food_id)s,
    %(allergen_id)s,
    %(strict)s
);
