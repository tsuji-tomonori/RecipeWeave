-- 検証済みバックアップの提案・調理履歴を元IDと全列で復元する。
INSERT INTO recipeweave.user_recipe_event (
    id,
    created_at,
    user_id,
    recipe_version_id,
    kind,
    occurred_at,
    request_key
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(recipe_version_id)s,
    %(kind)s,
    %(occurred_at)s,
    %(request_key)s
);
