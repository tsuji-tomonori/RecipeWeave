-- 参照先の展開済み工程が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.session_task AS t
WHERE
    t.id = %(reference_id)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    );
