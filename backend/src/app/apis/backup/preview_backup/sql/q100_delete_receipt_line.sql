-- 全置換の確認対象である本人のレシートの商品候補と確定した在庫の対応だけを削除する。
DELETE FROM recipeweave.receipt_line AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.receipt_import AS owner_0
    WHERE
        owner_0.id = t.import_id
        AND owner_0.user_id = %(actor_id)s
));
