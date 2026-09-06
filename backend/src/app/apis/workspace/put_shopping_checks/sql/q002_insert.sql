-- 食品と単位を参照して、数量不明を含む購入確認を保存する。
INSERT INTO recipeweave.user_shopping_check (
    id, user_id, key, signature, food_id, amount, unit_id, checked_at, archived
)
SELECT
    %(row_id)s,
    %(user_id)s,
    %(key)s,
    %(signature)s,
    %(food_id)s,
    %(amount)s,
    u.id,
    %(checked_at)s,
    %(archived)s
FROM recipeweave.unit AS u
WHERE u.code = %(unit)s AND u.status = 'active' RETURNING id;
