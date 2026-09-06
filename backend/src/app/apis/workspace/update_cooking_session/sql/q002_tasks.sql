-- 進捗更新の対象は本人のセッションに属する既存工程だけにする。
SELECT
    t.id,
    t.menu_item_id,
    t.step_id,
    t.status,
    t.timer_started_at,
    t.timer_duration_s,
    t.planned_start_s,
    t.planned_end_s
FROM recipeweave.session_task AS t
INNER JOIN recipeweave.cooking_session AS s ON t.session_id = s.id
INNER JOIN recipeweave.menu AS m ON s.menu_id = m.id
WHERE t.session_id = %(session_id)s AND m.user_id = %(user_id)s
ORDER BY t.planned_start_s, t.id;
