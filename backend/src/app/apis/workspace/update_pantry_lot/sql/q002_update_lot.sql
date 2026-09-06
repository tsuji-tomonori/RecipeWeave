-- 本人の編集可能なロットだけを更新し、取消済みレシートの在庫は復元しない。
UPDATE recipeweave.pantry_lot AS p SET
    form_id = %(form_id)s, amount = %(amount)s,
    unit_id = %(unit_id)s, expires_on = %(expires_on)s, location = %(location)s,
    priority = %(priority)s, quantity_quality = %(quality)s, status = 'active',
    updated_at = CURRENT_TIMESTAMP, edited = TRUE
WHERE
    p.id = %(row_id)s AND p.user_id = %(user_id)s
    AND (p.status = 'active' OR (p.status = 'deleted' AND %(restore)s))
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.receipt_import AS r
        WHERE r.id = p.source_import_id AND r.status = 'reverted'
    )
RETURNING p.id;
