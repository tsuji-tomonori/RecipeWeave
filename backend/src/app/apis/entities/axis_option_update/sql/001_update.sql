-- 軸候補値を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.axis_option AS t
SET
    axis_id = %(axis_id)s,
    code = %(code)s,
    label = %(label)s,
    definition = %(definition)s,
    parent_id = %(parent_id)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.axis_id,
    t.code,
    t.label,
    t.definition,
    t.parent_id,
    t.status,
    t.xmin::TEXT AS etag;
