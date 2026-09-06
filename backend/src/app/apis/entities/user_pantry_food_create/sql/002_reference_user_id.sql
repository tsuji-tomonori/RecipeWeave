-- 参照先のアプリ利用者が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.app_user AS t
WHERE
    t.id = %(reference_id)s
    AND t.id = %(actor_id)s;
