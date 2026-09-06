-- 調理工程ノードを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_step AS t
SET
    recipe_version_id = %(recipe_version_id)s,
    step_no = %(step_no)s,
    operation_id = %(operation_id)s,
    instruction = %(instruction)s,
    attention = %(attention)s,
    duration_min_s = %(duration_min_s)s,
    duration_max_s = %(duration_max_s)s,
    scaling_rule_id = %(scaling_rule_id)s,
    completion_cue = %(completion_cue)s,
    title = %(title)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.step_no,
    t.operation_id,
    t.instruction,
    t.attention,
    t.duration_min_s,
    t.duration_max_s,
    t.scaling_rule_id,
    t.completion_cue,
    t.title,
    t.xmin::TEXT AS etag;
