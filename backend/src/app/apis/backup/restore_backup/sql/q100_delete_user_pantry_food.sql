-- 全置換の確認対象である本人の利用者が常備すると設定した食材だけを削除する。
DELETE FROM recipeweave.user_pantry_food AS t
WHERE (t.user_id = %(actor_id)s);
