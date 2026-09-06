-- 買い物行を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.shopping_item AS t (
    id,
    session_id,
    total_id,
    product_version_id,
    net_shortage,
    package_count,
    surplus_amount,
    checked,
    client_key,
    checked_at,
    archived
)
VALUES (
    %(row_id)s,
    %(session_id)s,
    %(total_id)s,
    %(product_version_id)s,
    %(net_shortage)s,
    %(package_count)s,
    %(surplus_amount)s,
    %(checked)s,
    %(client_key)s,
    %(checked_at)s,
    %(archived)s
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
