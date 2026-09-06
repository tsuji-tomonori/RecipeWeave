-- 全置換の確認対象である本人の献立材料集計結果だけを削除する。
DELETE FROM recipeweave.ingredient_total AS t
WHERE (EXISTS (
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
));
