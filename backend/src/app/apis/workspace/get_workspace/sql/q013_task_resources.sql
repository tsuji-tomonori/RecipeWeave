-- タスクに必要な器具の表示名を読む。
SELECT
    t.id AS task_id,
    r.name
FROM recipeweave.session_task AS t
INNER JOIN recipeweave.step_resource AS sr ON t.step_id = sr.step_id
INNER JOIN recipeweave.resource_type AS r ON sr.resource_type_id = r.id
WHERE t.session_id = %(session_id)s AND r.code <> 'person'
ORDER BY t.id, r.name;
