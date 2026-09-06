-- レシートの商品候補と確定した在庫の対応を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
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
    t.xmin::TEXT AS etag
FROM recipeweave.receipt_line AS t
WHERE
    t.id = %(row_id)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.receipt_import AS owner_0
        WHERE
            owner_0.id = t.import_id
            AND owner_0.user_id = %(actor_id)s
    );
