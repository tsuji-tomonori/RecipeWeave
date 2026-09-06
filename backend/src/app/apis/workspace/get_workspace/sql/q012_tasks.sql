-- 調理工程とタイマーを正規化されたタスクから読む。
SELECT
    t.id,
    t.menu_item_id,
    t.step_id,
    t.planned_start_s,
    t.planned_end_s,
    t.duration_source,
    t.confirmed_duration_s,
    t.status,
    t.timer_started_at,
    t.timer_duration_s,
    rv.recipe_id,
    r.title AS recipe_name,
    st.title,
    st.instruction,
    st.attention,
    st.duration_max_s,
    scaling.mode AS scaling_mode
FROM recipeweave.session_task AS t INNER JOIN recipeweave.menu_item AS mi ON t.menu_item_id = mi.id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe AS r ON rv.recipe_id = r.id
INNER JOIN recipeweave.recipe_step AS st ON t.step_id = st.id
INNER JOIN recipeweave.scaling_rule AS scaling ON st.scaling_rule_id = scaling.id
WHERE t.session_id = %(session_id)s
ORDER BY t.planned_start_s, mi.position, st.step_no, t.id;
