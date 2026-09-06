-- 同じ形態・単位の確定数量だけを期限と登録順で消費候補にする。
SELECT
    id,
    amount
FROM recipeweave.pantry_lot
WHERE
    user_id = %(user_id)s AND form_id = %(form_id)s AND unit_id = %(unit_id)s
    AND product_version_id IS NOT DISTINCT FROM %(product_id)s
    AND status = 'active' AND quantity_quality = 'known' AND amount > 0
ORDER BY expires_on NULLS LAST, created_at, id FOR UPDATE;
