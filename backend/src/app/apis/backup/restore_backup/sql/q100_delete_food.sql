-- 全置換の確認対象である本人の購入・利用食材概念だけを削除する。
DELETE FROM recipeweave.food AS t
WHERE (t.owner_id = %(actor_id)s);
