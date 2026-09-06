-- AI生成方針版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_policy AS t (
    id,
    version,
    prompt_template,
    model_identifier,
    parameter_json,
    schema_version,
    release_id
)
VALUES (
    %(row_id)s,
    %(version)s,
    %(prompt_template)s,
    %(model_identifier)s,
    %(parameter_json)s,
    %(schema_version)s,
    %(release_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.version,
    t.prompt_template,
    t.model_identifier,
    t.parameter_json,
    t.schema_version,
    t.release_id,
    t.xmin::TEXT AS etag;
