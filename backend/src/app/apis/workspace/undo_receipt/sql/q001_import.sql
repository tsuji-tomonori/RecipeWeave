-- 本人のレシート状態を確認して再取消を防ぐ。
SELECT
    id,
    status
FROM recipeweave.receipt_import
WHERE id = %(row_id)s AND user_id = %(user_id)s FOR UPDATE;
