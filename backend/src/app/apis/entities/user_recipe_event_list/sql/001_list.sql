-- 提案・調理履歴を一覧取得する。
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
    t.user_id = %(actor_id)s
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
