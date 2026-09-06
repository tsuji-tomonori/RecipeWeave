-- 献立を条件付き削除する。
-- 値は名前付きパラメータで束縛する。
DELETE FROM recipeweave.menu AS t
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
