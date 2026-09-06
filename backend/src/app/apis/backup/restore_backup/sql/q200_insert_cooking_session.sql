-- 検証済みバックアップの調理計画実行を元IDと全列で復元する。
INSERT INTO recipeweave.cooking_session (
    id,
    created_at,
    menu_id,
    menu_revision,
    status,
    target_at,
    planner_version,
    input_snapshot,
    input_hash,
    current_task_index
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_id)s,
    %(menu_revision)s,
    %(status)s,
    %(target_at)s,
    %(planner_version)s,
    %(input_snapshot)s,
    %(input_hash)s,
    %(current_task_index)s
);
