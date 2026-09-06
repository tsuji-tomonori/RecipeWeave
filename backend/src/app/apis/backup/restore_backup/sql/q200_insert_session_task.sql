-- 検証済みバックアップの展開済み工程を元IDと全列で復元する。
INSERT INTO recipeweave.session_task (
    id,
    created_at,
    session_id,
    menu_item_id,
    step_id,
    batch_no,
    planned_start_s,
    planned_end_s,
    status,
    actual_start_at,
    actual_end_at,
    timer_started_at,
    timer_duration_s,
    duration_source,
    confirmed_duration_s
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(menu_item_id)s,
    %(step_id)s,
    %(batch_no)s,
    %(planned_start_s)s,
    %(planned_end_s)s,
    %(status)s,
    %(actual_start_at)s,
    %(actual_end_at)s,
    %(timer_started_at)s,
    %(timer_duration_s)s,
    %(duration_source)s,
    %(confirmed_duration_s)s
);
