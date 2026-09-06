-- 本人の進行中セッションを確認する。
SELECT
    s.id,
    s.menu_id,
    s.status,
    s.current_task_index
FROM recipeweave.cooking_session AS s
INNER JOIN
    recipeweave.menu AS m
    ON s.menu_id = m.id
WHERE
    m.user_id = %(user_id)s
    AND s.status IN ('planned', 'cooking', 'paused')
ORDER BY s.created_at DESC;
