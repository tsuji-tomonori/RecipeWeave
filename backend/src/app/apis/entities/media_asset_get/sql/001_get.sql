-- 教育用動画等の版を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
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
    t.xmin::TEXT AS etag
FROM recipeweave.media_asset AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
