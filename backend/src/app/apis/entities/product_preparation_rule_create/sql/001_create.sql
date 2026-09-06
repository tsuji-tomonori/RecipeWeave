-- 商品固有の調理条件を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product_preparation_rule AS t (
    id,
    product_version_id,
    operation_id,
    allowed,
    use_original_container,
    parameter_contract,
    source_id
)
VALUES (
    %(row_id)s,
    %(product_version_id)s,
    %(operation_id)s,
    %(allowed)s,
    %(use_original_container)s,
    %(parameter_contract)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.product_version_id,
    t.operation_id,
    t.allowed,
    t.use_original_container,
    t.parameter_contract,
    t.source_id,
    t.xmin::TEXT AS etag;
