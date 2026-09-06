-- 検証済み換算点を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.rule_id,
    t.servings,
    t.multiplier,
    t.xmin::TEXT AS etag
FROM recipeweave.scaling_point AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
