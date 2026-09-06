-- 標準調理動作を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.operation AS t (
    id,
    code,
    name,
    definition,
    precondition,
    completion_cue,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(definition)s,
    %(precondition)s,
    %(completion_cue)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.definition,
    t.precondition,
    t.completion_cue,
    t.status,
    t.xmin::TEXT AS etag;
