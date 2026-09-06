-- 料理同一性上の食品を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.normalizer_version,
    t.xmin::TEXT AS etag
FROM recipeweave.food_identity AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
