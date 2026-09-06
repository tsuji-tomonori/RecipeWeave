-- セット内構成品を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.product_version_id,
    t.form_id,
    t.name,
    t.amount,
    t.unit_id,
    t.quality,
    t.xmin::TEXT AS etag
FROM recipeweave.product_component AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
