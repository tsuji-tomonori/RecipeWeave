-- 検証済みバックアップの献立展開後依存を元IDと全列で復元する。
INSERT INTO recipeweave.task_dependency (
    id,
    created_at,
    before_task_id,
    after_task_id,
    min_lag_s,
    max_lag_s,
    reason
) VALUES (
    %(id)s,
    %(created_at)s,
    %(before_task_id)s,
    %(after_task_id)s,
    %(min_lag_s)s,
    %(max_lag_s)s,
    %(reason)s
);
