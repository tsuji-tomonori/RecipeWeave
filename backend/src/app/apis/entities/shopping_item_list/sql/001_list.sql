-- 買い物行を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.session_id,
    t.total_id,
    t.product_version_id,
    t.net_shortage,
    t.package_count,
    t.surplus_amount,
    t.checked,
    t.client_key,
    t.checked_at,
    t.archived,
    t.xmin::TEXT AS etag
FROM recipeweave.shopping_item AS t
WHERE
    EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    )
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
