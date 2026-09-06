-- カタログ公開版を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.version,
    t.manifest_hash,
    t.published_at,
    t.xmin::TEXT AS etag
FROM recipeweave.catalog_release AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
