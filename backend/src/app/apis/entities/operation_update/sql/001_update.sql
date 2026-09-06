-- 標準調理動作を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.operation AS t
SET
    code = %(code)s,
    name = %(name)s,
    definition = %(definition)s,
    precondition = %(precondition)s,
    completion_cue = %(completion_cue)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
