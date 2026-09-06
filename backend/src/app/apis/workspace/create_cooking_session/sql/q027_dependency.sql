-- 工程の先行条件を具体的なタスク間に移す。
INSERT INTO recipeweave.task_dependency (
    id, before_task_id, after_task_id, min_lag_s, max_lag_s, reason
)
VALUES (%(row_id)s, %(before_id)s, %(after_id)s, %(min_lag)s, %(max_lag)s, %(reason)s);
