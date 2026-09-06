-- 買い物行を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.shopping_item AS t
SET
    session_id = %(session_id)s,
    total_id = %(total_id)s,
    product_version_id = %(product_version_id)s,
    net_shortage = %(net_shortage)s,
    package_count = %(package_count)s,
    surplus_amount = %(surplus_amount)s,
    checked = %(checked)s,
    client_key = %(client_key)s,
    checked_at = %(checked_at)s,
    archived = %(archived)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
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
RETURNING
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
    t.xmin::TEXT AS etag;
