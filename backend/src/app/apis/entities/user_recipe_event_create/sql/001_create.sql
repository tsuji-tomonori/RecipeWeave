-- 提案・調理履歴を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_recipe_event AS t (
    id,
    user_id,
    recipe_version_id,
    kind,
    occurred_at,
    request_key
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(recipe_version_id)s,
    %(kind)s,
    %(occurred_at)s,
    %(request_key)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.recipe_version_id,
    t.kind,
    t.occurred_at,
    t.request_key,
    t.xmin::TEXT AS etag;
