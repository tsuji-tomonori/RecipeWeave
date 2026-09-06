-- 展開済み工程を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.session_task AS t
SET
    session_id = %(session_id)s,
    menu_item_id = %(menu_item_id)s,
    step_id = %(step_id)s,
    batch_no = %(batch_no)s,
    planned_start_s = %(planned_start_s)s,
    planned_end_s = %(planned_end_s)s,
    status = %(status)s,
    actual_start_at = %(actual_start_at)s,
    actual_end_at = %(actual_end_at)s,
    timer_started_at = %(timer_started_at)s,
    timer_duration_s = %(timer_duration_s)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
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
    t.xmin::TEXT AS etag;
