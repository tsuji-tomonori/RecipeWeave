-- 調理開始前にも利用できる本人の買い物確認を読む。
SELECT
    c.key AS client_key,
    c.signature,
    c.food_id,
    c.amount,
    u.code AS unit,
    c.checked_at,
    c.archived
FROM recipeweave.user_shopping_check AS c INNER JOIN recipeweave.unit AS u ON c.unit_id = u.id
WHERE c.user_id = %(user_id)s
ORDER BY c.checked_at, c.id;
