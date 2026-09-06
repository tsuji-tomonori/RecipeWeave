-- セット内構成品を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product_component AS t (
    id,
    product_version_id,
    form_id,
    name,
    amount,
    unit_id,
    quality
)
VALUES (
    %(row_id)s,
    %(product_version_id)s,
    %(form_id)s,
    %(name)s,
    %(amount)s,
    %(unit_id)s,
    %(quality)s
)
RETURNING
    t.id,
    t.created_at,
    t.product_version_id,
    t.form_id,
    t.name,
    t.amount,
    t.unit_id,
    t.quality,
    t.xmin::TEXT AS etag;
