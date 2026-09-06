-- レシート読取・在庫登録の処理単位を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.receipt_import AS t
SET
    user_id = %(user_id)s,
    file_sha256 = %(file_sha256)s,
    idempotency_key = %(idempotency_key)s,
    status = %(status)s,
    revision = %(revision)s,
    committed_at = %(committed_at)s,
    reverted_at = %(reverted_at)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.file_sha256,
    t.idempotency_key,
    t.status,
    t.revision,
    t.committed_at,
    t.reverted_at,
    t.xmin::TEXT AS etag;
