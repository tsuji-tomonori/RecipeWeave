-- 全置換の確認対象である本人の食材別名だけを削除する。
DELETE FROM recipeweave.food_alias AS t
WHERE (EXISTS (
    SELECT 1 FROM recipeweave.food AS food
    WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
));
