-- 全置換の確認対象である本人の献立別材料確定だけを削除する。
DELETE FROM recipeweave.menu_ingredient_override AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.menu_item AS owner_0
    WHERE
        owner_0.id = t.menu_item_id
        AND EXISTS (
            SELECT owner_1.id
            FROM recipeweave.menu AS owner_1
            WHERE
                owner_1.id = owner_0.menu_id
                AND owner_1.user_id = %(actor_id)s
        )
));
