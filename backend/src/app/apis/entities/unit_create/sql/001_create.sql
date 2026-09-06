-- 単位を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.unit AS t (
    id,
    code,
    name,
    dimension,
    factor,
    "offset",
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(dimension)s,
    %(factor)s,
    %(offset)s,
    %(status)s
)
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
