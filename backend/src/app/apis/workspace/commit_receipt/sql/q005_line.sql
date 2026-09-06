-- 利用者が選択した商品だけを、登録ロットと対応付けて残す。
INSERT INTO recipeweave.receipt_line (
    id, import_id, line_no, raw_name, form_id, amount, unit_id, decision, pantry_lot_id
)
VALUES (
    %(row_id)s,
    %(import_id)s,
    %(line_no)s,
    %(name)s,
    %(form_id)s,
    %(amount)s,
    %(unit_id)s,
    'accepted',
    %(lot_id)s
);
