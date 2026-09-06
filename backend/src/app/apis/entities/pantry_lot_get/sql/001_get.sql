-- 手持ち食材ロットを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.form_id,
    t.product_version_id,
    t.amount,
    t.unit_id,
    t.expires_on,
    t.opened_at,
    t.location,
    t.priority,
    t.status,
    t.source_import_id,
    t.quantity_quality,
    t.original_form_id,
    t.original_amount,
    t.original_unit_id,
    t.updated_at,
    t.edited,
    t.xmin::TEXT AS etag
FROM recipeweave.pantry_lot AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
