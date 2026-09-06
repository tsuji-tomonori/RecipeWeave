-- 登録時の値と現在値を一緒に記録する。不明数量はNULLのまま保持する。
INSERT INTO recipeweave.pantry_lot
(
    id, user_id, form_id, amount, unit_id, expires_on, location, priority, source_import_id,
    quantity_quality, original_form_id, original_amount, original_unit_id
)
VALUES (
    %(row_id)s, %(user_id)s, %(form_id)s, %(amount)s, %(unit_id)s, %(expires_on)s,
    %(location)s, %(priority)s, %(import_id)s, %(quality)s, %(form_id)s, %(amount)s, %(unit_id)s
)
RETURNING id;
