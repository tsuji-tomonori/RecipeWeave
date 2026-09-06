-- 全置換の確認対象である本人の商品仕様版だけを削除する。
DELETE FROM recipeweave.product_version AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.product AS product ON food.id = product.food_id
        WHERE product.id = t.product_id AND food.owner_id = %(actor_id)s
    ));
