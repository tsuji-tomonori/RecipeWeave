-- 検証済みバックアップの食材の分類属性を元IDと全列で復元する。
INSERT INTO recipeweave.food_axis_option (
    id,
    created_at,
    food_id,
    option_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(option_id)s
);
