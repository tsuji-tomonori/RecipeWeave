-- 展開済み工程を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.session_task AS t (
    id,
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
)
VALUES (
    %(row_id)s,
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
)
RETURNING
    t.id,
    t.created_at,
    t.session_id,
    t.menu_item_id,
    t.step_id,
    t.batch_no,
    t.planned_start_s,
    t.planned_end_s,
    t.status,
    t.actual_start_at,
    t.actual_end_at,
    t.timer_started_at,
    t.timer_duration_s,
    t.duration_source,
    t.confirmed_duration_s,
    t.xmin::TEXT AS etag;
