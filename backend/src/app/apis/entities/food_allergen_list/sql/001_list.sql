-- 食材アレルゲン知識を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.form_id,
    t.allergen_id,
    t.presence,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.food_allergen AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
