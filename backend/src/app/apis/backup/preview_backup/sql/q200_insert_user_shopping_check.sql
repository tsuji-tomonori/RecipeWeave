-- 検証済みバックアップの調理前の買い物確認を元IDと全列で復元する。
INSERT INTO recipeweave.user_shopping_check (
    id,
    created_at,
    user_id,
    key,
    signature,
    food_id,
    amount,
    unit_id,
    checked_at,
    archived
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(key)s,
    %(signature)s,
    %(food_id)s,
    %(amount)s,
    %(unit_id)s,
    %(checked_at)s,
    %(archived)s
);
