-- 購入・利用食材概念を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.kind,
    t.parent_id,
    t.release_id,
    t.status,
    t.owner_id,
    t.xmin::TEXT AS etag
FROM recipeweave.food AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
