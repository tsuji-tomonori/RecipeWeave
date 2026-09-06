-- 手持ち食材ロットを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.pantry_lot AS t
SET
    user_id = %(user_id)s,
    form_id = %(form_id)s,
    product_version_id = %(product_version_id)s,
    amount = %(amount)s,
    unit_id = %(unit_id)s,
    expires_on = %(expires_on)s,
    opened_at = %(opened_at)s,
    location = %(location)s,
    priority = %(priority)s,
    status = %(status)s,
    source_import_id = %(source_import_id)s,
    quantity_quality = %(quantity_quality)s,
    original_form_id = %(original_form_id)s,
    original_amount = %(original_amount)s,
    original_unit_id = %(original_unit_id)s,
    updated_at = %(updated_at)s,
    edited = %(edited)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
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
    t.xmin::TEXT AS etag;
