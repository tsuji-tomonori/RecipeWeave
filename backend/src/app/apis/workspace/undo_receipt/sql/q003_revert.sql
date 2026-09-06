-- 取消済みのレシートを再び登録状態へ戻さない。
UPDATE recipeweave.receipt_import SET
    status = 'reverted', reverted_at = CURRENT_TIMESTAMP, revision = revision + 1
WHERE id = %(row_id)s AND user_id = %(user_id)s AND status = 'committed' RETURNING id;
