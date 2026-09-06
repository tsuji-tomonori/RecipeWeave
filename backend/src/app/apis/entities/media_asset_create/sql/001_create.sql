-- 教育用動画等の版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.media_asset AS t (
    id,
    operation_id,
    media_type,
    uri,
    sha256,
    locale,
    version,
    parameter_contract,
    source_id,
    validation
)
VALUES (
    %(row_id)s,
    %(operation_id)s,
    %(media_type)s,
    %(uri)s,
    %(sha256)s,
    %(locale)s,
    %(version)s,
    %(parameter_contract)s,
    %(source_id)s,
    %(validation)s
)
RETURNING
    t.id,
    t.created_at,
    t.operation_id,
    t.media_type,
    t.uri,
    t.sha256,
    t.locale,
    t.version,
    t.parameter_contract,
    t.source_id,
    t.validation,
    t.xmin::TEXT AS etag;
