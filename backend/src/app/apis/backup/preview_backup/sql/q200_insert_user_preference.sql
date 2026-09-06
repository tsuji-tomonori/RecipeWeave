-- 検証済みバックアップのユーザーの嗜好を元IDと全列で復元する。
INSERT INTO recipeweave.user_preference (
    id,
    created_at,
    user_id,
    option_id,
    weight
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(option_id)s,
    %(weight)s
);
