-- 軸候補値を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.axis_id,
    t.code,
    t.label,
    t.definition,
    t.parent_id,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.axis_option AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
