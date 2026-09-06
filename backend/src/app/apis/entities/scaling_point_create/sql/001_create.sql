-- 検証済み換算点を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.scaling_point AS t (
    id,
    rule_id,
    servings,
    multiplier
)
VALUES (
    %(row_id)s,
    %(rule_id)s,
    %(servings)s,
    %(multiplier)s
)
RETURNING
    t.id,
    t.created_at,
    t.rule_id,
    t.servings,
    t.multiplier,
    t.xmin::TEXT AS etag;
