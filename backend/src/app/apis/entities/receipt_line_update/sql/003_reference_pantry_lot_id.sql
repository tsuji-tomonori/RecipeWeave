-- 参照先の手持ち食材ロットが同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.pantry_lot AS t
WHERE
    t.id = %(reference_id)s
    AND t.user_id = %(actor_id)s;
