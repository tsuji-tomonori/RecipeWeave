-- 調理計画実行を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.cooking_session AS t (
    id,
    menu_id,
    menu_revision,
    status,
    target_at,
    planner_version,
    input_snapshot,
    input_hash,
    current_task_index
)
VALUES (
    %(row_id)s,
    %(menu_id)s,
    %(menu_revision)s,
    %(status)s,
    %(target_at)s,
    %(planner_version)s,
    %(input_snapshot)s,
    %(input_hash)s,
    %(current_task_index)s
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
