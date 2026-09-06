-- AI生成方針版を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.version,
    t.prompt_template,
    t.model_identifier,
    t.parameter_json,
    t.schema_version,
    t.release_id,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_policy AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
