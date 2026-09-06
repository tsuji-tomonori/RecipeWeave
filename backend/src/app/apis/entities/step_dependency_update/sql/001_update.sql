-- 工程依存辺を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.step_dependency AS t
SET
    before_step_id = %(before_step_id)s,
    after_step_id = %(after_step_id)s,
    kind = %(kind)s,
    min_lag_s = %(min_lag_s)s,
    max_lag_s = %(max_lag_s)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.before_step_id,
    t.after_step_id,
    t.kind,
    t.min_lag_s,
    t.max_lag_s,
    t.xmin::TEXT AS etag;
