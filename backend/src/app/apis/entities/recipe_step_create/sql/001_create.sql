-- 調理工程ノードを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_step AS t (
    id,
    recipe_version_id,
    step_no,
    operation_id,
    instruction,
    attention,
    duration_min_s,
    duration_max_s,
    scaling_rule_id,
    completion_cue,
    title
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(step_no)s,
    %(operation_id)s,
    %(instruction)s,
    %(attention)s,
    %(duration_min_s)s,
    %(duration_max_s)s,
    %(scaling_rule_id)s,
    %(completion_cue)s,
    %(title)s
)
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
