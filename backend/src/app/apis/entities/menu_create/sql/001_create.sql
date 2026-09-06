-- 献立を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.menu AS t (
    id,
    user_id,
    name,
    servings,
    revision
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(name)s,
    %(servings)s,
    1
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.name,
    t.servings,
    t.revision,
    t.xmin::TEXT AS etag;
