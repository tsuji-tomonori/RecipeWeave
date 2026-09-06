-- 軸候補値を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.axis_option AS t (
    id,
    axis_id,
    code,
    label,
    definition,
    parent_id,
    status
)
VALUES (
    %(row_id)s,
    %(axis_id)s,
    %(code)s,
    %(label)s,
    %(definition)s,
    %(parent_id)s,
    %(status)s
)
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
