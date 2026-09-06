-- 献立展開後依存を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.task_dependency AS t (
    id,
    before_task_id,
    after_task_id,
    min_lag_s,
    max_lag_s,
    reason
)
VALUES (
    %(row_id)s,
    %(before_task_id)s,
    %(after_task_id)s,
    %(min_lag_s)s,
    %(max_lag_s)s,
    %(reason)s
)
RETURNING
    t.id,
    t.created_at,
    t.before_task_id,
    t.after_task_id,
    t.min_lag_s,
    t.max_lag_s,
    t.reason,
    t.xmin::TEXT AS etag;
