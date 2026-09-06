-- 全置換の確認対象である本人の食材アレルゲン知識だけを削除する。
DELETE FROM recipeweave.food_allergen AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
        WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
    ));
