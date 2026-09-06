-- 全置換の確認対象である本人の資源の予約だけを削除する。
DELETE FROM recipeweave.resource_reservation AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.session_task AS owner_0
    WHERE
        owner_0.id = t.task_id
        AND EXISTS (
            SELECT owner_1.id
            FROM recipeweave.cooking_session AS owner_1
            WHERE
                owner_1.id = owner_0.session_id
                AND EXISTS (
                    SELECT owner_2.id
                    FROM recipeweave.menu AS owner_2
                    WHERE
                        owner_2.id = owner_1.menu_id
                        AND owner_2.user_id = %(actor_id)s
                )
        )
));
