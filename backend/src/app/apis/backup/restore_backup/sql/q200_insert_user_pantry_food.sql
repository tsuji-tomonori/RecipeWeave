-- 検証済みバックアップの利用者が常備すると設定した食材を元IDと全列で復元する。
INSERT INTO recipeweave.user_pantry_food (
    id,
    created_at,
    user_id,
    food_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(food_id)s
);
