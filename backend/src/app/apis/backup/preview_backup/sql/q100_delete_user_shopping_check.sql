-- 全置換の確認対象である本人の調理前の買い物確認だけを削除する。
DELETE FROM recipeweave.user_shopping_check AS t
WHERE (t.user_id = %(actor_id)s);
