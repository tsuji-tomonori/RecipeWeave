-- 商品表示アレルゲンを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product_allergen AS t (
    id,
    product_version_id,
    allergen_id,
    presence,
    source_id
)
VALUES (
    %(row_id)s,
    %(product_version_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.product_version_id,
    t.allergen_id,
    t.presence,
    t.source_id,
    t.xmin::TEXT AS etag;
