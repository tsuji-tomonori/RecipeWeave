-- 開始済みタイマーを再送でリセットしない。
UPDATE recipeweave.session_task SET
    timer_started_at = CURRENT_TIMESTAMP,
    timer_duration_s = planned_end_s - planned_start_s
WHERE id = %(row_id)s AND session_id = %(session_id)s AND timer_started_at IS NULL;
