-- 全置換の確認対象である本人の利用者が追加した独自食材の所有だけを削除する。
DELETE FROM recipeweave.user_food AS t
WHERE (t.user_id = %(actor_id)s);
