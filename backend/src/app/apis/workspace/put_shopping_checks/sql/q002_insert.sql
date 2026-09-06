-- 食品と単位を参照して、数量不明を含む購入確認を保存する。
INSERT INTO recipeweave.user_shopping_check (
    id, user_id, key, signature, food_id, amount, unit_id, checked_at, archived
)
SELECT
    %(row_id)s AS id,
    %(user_id)s AS user_id,
    %(key)s AS key,
    %(signature)s AS signature,
    %(food_id)s AS food_id,
    %(amount)s AS amount,
    u.id AS unit_id,
    %(checked_at)s AS checked_at,
    %(archived)s AS archived
FROM recipeweave.unit AS u
WHERE u.code = %(unit)s AND u.status = 'active' RETURNING id;
