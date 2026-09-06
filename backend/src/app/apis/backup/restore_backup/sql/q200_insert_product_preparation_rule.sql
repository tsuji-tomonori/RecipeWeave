-- 検証済みバックアップの商品固有の調理条件を元IDと全列で復元する。
INSERT INTO recipeweave.product_preparation_rule (
    id,
    created_at,
    product_version_id,
    operation_id,
    allowed,
    use_original_container,
    parameter_contract,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(operation_id)s,
    %(allowed)s,
    %(use_original_container)s,
    %(parameter_contract)s,
    %(source_id)s
);
