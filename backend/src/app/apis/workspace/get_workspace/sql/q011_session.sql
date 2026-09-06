-- 本人の直近の調理を読む。入力の料理はセッション専用献立に固定済み。
SELECT
    s.id,
    s.menu_id,
    s.status,
    s.current_task_index,
    s.input_snapshot
FROM recipeweave.cooking_session AS s INNER JOIN recipeweave.menu AS m ON s.menu_id = m.id
WHERE m.user_id = %(user_id)s AND s.status <> 'cancelled'
ORDER BY s.created_at DESC, s.id DESC
LIMIT 1;
