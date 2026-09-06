-- 検証済みバックアップのレシートの商品候補と確定した在庫の対応を元IDと全列で復元する。
INSERT INTO recipeweave.receipt_line (
    id,
    created_at,
    import_id,
    line_no,
    raw_name,
    form_id,
    product_version_id,
    amount,
    unit_id,
    decision,
    pantry_lot_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(import_id)s,
    %(line_no)s,
    %(raw_name)s,
    %(form_id)s,
    %(product_version_id)s,
    %(amount)s,
    %(unit_id)s,
    %(decision)s,
    %(pantry_lot_id)s
);
