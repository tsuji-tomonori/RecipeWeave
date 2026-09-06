-- 全置換の確認対象である本人の提案・調理履歴だけを削除する。
DELETE FROM recipeweave.user_recipe_event AS t
WHERE (t.user_id = %(actor_id)s);
