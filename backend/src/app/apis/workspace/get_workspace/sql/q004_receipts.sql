-- 画像本文を保存せず、重複検知と取消しに必要な履歴だけを読む。
SELECT
    r.id,
    r.file_sha256,
    r.idempotency_key,
    r.created_at,
    r.status,
    r.reverted_at
FROM
    recipeweave.receipt_import AS r
WHERE
    r.user_id = %(user_id)s
    AND r.status IN ('committed', 'reverted')
ORDER BY r.created_at, r.id;
