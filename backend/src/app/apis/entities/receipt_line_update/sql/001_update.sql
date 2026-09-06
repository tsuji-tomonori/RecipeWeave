-- レシートの商品候補と確定した在庫の対応を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.receipt_line AS t
SET
    import_id = %(import_id)s,
    line_no = %(line_no)s,
    raw_name = %(raw_name)s,
    form_id = %(form_id)s,
    product_version_id = %(product_version_id)s,
    amount = %(amount)s,
    unit_id = %(unit_id)s,
    decision = %(decision)s,
    pantry_lot_id = %(pantry_lot_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.receipt_import AS owner_0
        WHERE
            owner_0.id = t.import_id
            AND owner_0.user_id = %(actor_id)s
    )
RETURNING
    t.id,
    t.created_at,
    t.import_id,
    t.line_no,
    t.raw_name,
    t.form_id,
    t.product_version_id,
    t.amount,
    t.unit_id,
    t.decision,
    t.pantry_lot_id,
    t.xmin::TEXT AS etag;
