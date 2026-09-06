-- 食材形態を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.food_id,
    t.name,
    t.state,
    t.base_unit_id,
    t.quantity_basis,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.food_form AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
