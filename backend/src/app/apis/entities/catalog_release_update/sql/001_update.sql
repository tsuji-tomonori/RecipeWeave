-- カタログ公開版を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.catalog_release AS t
SET
    version = %(version)s,
    manifest_hash = %(manifest_hash)s,
    published_at = %(published_at)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.version,
    t.manifest_hash,
    t.published_at,
    t.owner_id,
    t.xmin::TEXT AS etag;
