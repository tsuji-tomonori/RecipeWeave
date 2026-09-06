-- 消費・編集済み在庫を巻き戻さず、未使用の登録分だけを取り消す。
UPDATE recipeweave.pantry_lot AS p SET status = 'undone', updated_at = CURRENT_TIMESTAMP
WHERE
    p.source_import_id = %(row_id)s AND p.user_id = %(user_id)s AND NOT p.edited
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.pantry_consumption AS c
        WHERE c.lot_id = p.id
    )
RETURNING p.id;
