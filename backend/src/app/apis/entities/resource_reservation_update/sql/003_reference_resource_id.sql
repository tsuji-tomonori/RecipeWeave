-- 参照先のキッチンの実資源が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.kitchen_resource AS t
WHERE
    t.id = %(reference_id)s
    AND t.user_id = %(actor_id)s;
