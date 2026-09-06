-- 標準調理動作を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.definition,
    t.precondition,
    t.completion_cue,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.operation AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
