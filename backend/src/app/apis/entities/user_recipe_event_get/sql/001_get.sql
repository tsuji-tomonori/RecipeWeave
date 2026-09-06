-- 提案・調理履歴を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.recipe_version_id,
    t.kind,
    t.occurred_at,
    t.request_key,
    t.xmin::TEXT AS etag
FROM recipeweave.user_recipe_event AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
