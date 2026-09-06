-- 検証済みバックアップのカタログ公開版を元IDと全列で復元する。
INSERT INTO recipeweave.catalog_release (
    id,
    created_at,
    version,
    manifest_hash,
    published_at,
    owner_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(version)s,
    %(manifest_hash)s,
    %(published_at)s,
    %(owner_id)s
);
