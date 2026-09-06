-- 検証済みバックアップの商品仕様版を元IDと全列で復元する。
INSERT INTO recipeweave.product_version (
    id,
    created_at,
    product_id,
    version,
    form_id,
    net_amount,
    unit_id,
    drain_amount,
    source_id,
    preparation_note,
    valid_from
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_id)s,
    %(version)s,
    %(form_id)s,
    %(net_amount)s,
    %(unit_id)s,
    %(drain_amount)s,
    %(source_id)s,
    %(preparation_note)s,
    %(valid_from)s
);
