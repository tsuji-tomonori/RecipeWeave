-- 全置換の確認対象である本人のキッチンの実資源だけを削除する。
DELETE FROM recipeweave.kitchen_resource AS t
WHERE (t.user_id = %(actor_id)s);
