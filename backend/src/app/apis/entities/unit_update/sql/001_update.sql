-- 単位を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.unit AS t
SET
    code = %(code)s,
    name = %(name)s,
    dimension = %(dimension)s,
    factor = %(factor)s,
    "offset" = %(offset)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.dimension,
    t.factor,
    t."offset",
    t.status,
    t.xmin::TEXT AS etag;
