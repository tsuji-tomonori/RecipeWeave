-- 全置換の確認対象である本人の形態・商品別栄養値だけを削除する。
DELETE FROM recipeweave.nutrition_fact AS t
WHERE
    (
        EXISTS (
            SELECT 1
            FROM recipeweave.food AS food
            INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
            WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
        )
        OR EXISTS (
            SELECT 1
            FROM recipeweave.food AS food
            INNER JOIN recipeweave.product AS product ON food.id = product.food_id
            INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
            WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
        )
    );
