-- 全置換の確認対象である本人の献立の料理だけを削除する。
DELETE FROM recipeweave.menu_item AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.menu AS owner_0
    WHERE
        owner_0.id = t.menu_id
        AND owner_0.user_id = %(actor_id)s
));
