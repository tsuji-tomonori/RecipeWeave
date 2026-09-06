-- カタログ公開版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.catalog_release AS t (
    id,
    version,
    manifest_hash,
    published_at
)
VALUES (
    %(row_id)s,
    %(version)s,
    %(manifest_hash)s,
    %(published_at)s
)
RETURNING
    t.id,
    t.created_at,
    t.version,
    t.manifest_hash,
    t.published_at,
    t.xmin::TEXT AS etag;
