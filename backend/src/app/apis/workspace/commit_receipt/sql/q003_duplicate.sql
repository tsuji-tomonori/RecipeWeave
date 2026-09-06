-- 画像と購入品構成の重複を本人の履歴だけで検出する。
SELECT
    id,
    status
FROM recipeweave.receipt_import
WHERE
    user_id = %(user_id)s
    AND (id = %(import_id)s OR file_sha256 = %(hash)s OR idempotency_key LIKE %(signature)s)
ORDER BY created_at;
