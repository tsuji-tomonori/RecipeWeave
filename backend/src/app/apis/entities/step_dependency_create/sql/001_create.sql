-- 工程依存辺を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_dependency AS t (
    id,
    before_step_id,
    after_step_id,
    kind,
    min_lag_s,
    max_lag_s
)
VALUES (
    %(row_id)s,
    %(before_step_id)s,
    %(after_step_id)s,
    %(kind)s,
    %(min_lag_s)s,
    %(max_lag_s)s
)
RETURNING
    t.id,
    t.created_at,
    t.before_step_id,
    t.after_step_id,
    t.kind,
    t.min_lag_s,
    t.max_lag_s,
    t.xmin::TEXT AS etag;
