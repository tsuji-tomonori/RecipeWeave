-- 商品仕様版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product_version AS t (
    id,
    product_id,
    version,
    form_id,
    net_amount,
    unit_id,
    drain_amount,
    source_id,
    preparation_note,
    valid_from
)
VALUES (
    %(row_id)s,
    %(product_id)s,
    %(version)s,
    %(form_id)s,
    %(net_amount)s,
    %(unit_id)s,
    %(drain_amount)s,
    %(source_id)s,
    %(preparation_note)s,
    %(valid_from)s
)
RETURNING
    t.id,
    t.created_at,
    t.product_id,
    t.version,
    t.form_id,
    t.net_amount,
    t.unit_id,
    t.drain_amount,
    t.source_id,
    t.preparation_note,
    t.valid_from,
    t.xmin::TEXT AS etag;
