-- 工程依存辺を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.before_step_id,
    t.after_step_id,
    t.kind,
    t.min_lag_s,
    t.max_lag_s,
    t.xmin::TEXT AS etag
FROM recipeweave.step_dependency AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
