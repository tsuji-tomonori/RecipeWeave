-- 参照先の献立が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.menu AS t
WHERE
    t.id = %(reference_id)s
    AND t.user_id = %(actor_id)s;
