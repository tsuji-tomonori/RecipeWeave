-- 計画済み工程を独立したタスク行へ保存する。
INSERT INTO recipeweave.session_task
(
    id, session_id, menu_item_id, step_id, batch_no, planned_start_s, planned_end_s, status,
    duration_source, confirmed_duration_s
)
VALUES (
    %(row_id)s, %(session_id)s, %(item_id)s, %(step_id)s, 1, %(start)s, %(end)s, 'pending',
    %(duration_source)s, %(confirmed_duration_s)s
);
