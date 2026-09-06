-- 検証済みバックアップの食材別名を元IDと全列で復元する。
INSERT INTO recipeweave.food_alias (
    id,
    created_at,
    food_id,
    alias,
    locale
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(alias)s,
    %(locale)s
);
