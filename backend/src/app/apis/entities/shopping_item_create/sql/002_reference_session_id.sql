-- 参照先の調理計画実行が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.cooking_session AS t
WHERE
    t.id = %(reference_id)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    );
