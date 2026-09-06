-- 全置換の確認対象である本人のレシート読取・在庫登録の処理単位だけを削除する。
DELETE FROM recipeweave.receipt_import AS t
WHERE (t.user_id = %(actor_id)s);
