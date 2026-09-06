-- 保存・解除は本人の追記イベントとして残す。
INSERT INTO recipeweave.user_recipe_event (
    id, user_id, recipe_version_id, kind, occurred_at, request_key
)
VALUES (%(row_id)s, %(user_id)s, %(version_id)s, 'disliked', CLOCK_TIMESTAMP(), %(request_key)s);
