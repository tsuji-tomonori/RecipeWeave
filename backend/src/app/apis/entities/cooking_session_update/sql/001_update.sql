-- 調理計画実行を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.cooking_session AS t
SET
    menu_id = %(menu_id)s,
    menu_revision = %(menu_revision)s,
    status = %(status)s,
    target_at = %(target_at)s,
    planner_version = %(planner_version)s,
    input_snapshot = %(input_snapshot)s,
    input_hash = %(input_hash)s,
    current_task_index = %(current_task_index)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    )
RETURNING
    t.id,
    t.created_at,
    t.menu_id,
    t.menu_revision,
    t.status,
    t.target_at,
    t.planner_version,
    t.input_snapshot,
    t.input_hash,
    t.current_task_index,
    t.xmin::TEXT AS etag;
