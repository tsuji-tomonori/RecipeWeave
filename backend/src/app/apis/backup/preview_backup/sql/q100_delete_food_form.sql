-- 全置換の確認対象である本人の食材形態だけを削除する。
DELETE FROM recipeweave.food_form AS t
WHERE (EXISTS (
    SELECT 1 FROM recipeweave.food AS food
    WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
));
