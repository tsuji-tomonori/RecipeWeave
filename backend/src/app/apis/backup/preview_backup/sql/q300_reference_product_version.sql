-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.product_version AS t
WHERE
    t.id = ANY(%(reference_ids)s::UUID[])
    AND (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.product AS product ON food.id = product.food_id
        WHERE product.id = t.product_id AND food.owner_id IS NULL
    ));
