-- 献立を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.menu AS t
SET
    user_id = %(user_id)s,
    name = %(name)s,
    servings = %(servings)s,
    revision = t.revision + 1
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.name,
    t.servings,
    t.revision,
    t.xmin::TEXT AS etag;
