-- 検証済みバックアップの買い物行を元IDと全列で復元する。
INSERT INTO recipeweave.shopping_item (
    id,
    created_at,
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
) VALUES (
    %(id)s,
    %(created_at)s,
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
);
