-- 検証済みバックアップの献立を元IDと全列で復元する。
INSERT INTO recipeweave.menu (
    id,
    created_at,
    user_id,
    name,
    servings,
    revision
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(name)s,
    %(servings)s,
    %(revision)s
);
