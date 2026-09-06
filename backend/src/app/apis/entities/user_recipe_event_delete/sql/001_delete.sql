-- 提案・調理履歴を条件付き削除する。
-- 値は名前付きパラメータで束縛する。
DELETE FROM recipeweave.user_recipe_event AS t
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.recipe_version_id,
    t.kind,
    t.occurred_at,
    t.request_key,
    t.xmin::TEXT AS etag;
