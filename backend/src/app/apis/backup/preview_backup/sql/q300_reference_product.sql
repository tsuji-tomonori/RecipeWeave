-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.product AS t
WHERE
    t.id = ANY(%(reference_ids)s::UUID[]) AND (EXISTS (
        SELECT 1 FROM recipeweave.food AS food
        WHERE food.id = t.food_id AND food.owner_id IS NULL
    ));
