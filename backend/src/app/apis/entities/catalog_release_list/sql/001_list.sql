-- カタログ公開版を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.version,
    t.manifest_hash,
    t.published_at,
    t.owner_id,
    t.xmin::TEXT AS etag
FROM recipeweave.catalog_release AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
