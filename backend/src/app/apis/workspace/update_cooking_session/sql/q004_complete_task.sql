-- 確認した工程を完了にし、最初の開始・完了時刻を保持する。
UPDATE recipeweave.session_task SET
    status = 'completed',
    actual_start_at = COALESCE(actual_start_at, CURRENT_TIMESTAMP),
    actual_end_at = COALESCE(actual_end_at, CURRENT_TIMESTAMP)
WHERE id = %(row_id)s AND session_id = %(session_id)s;
