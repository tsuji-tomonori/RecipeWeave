-- レシート読取・在庫登録の処理単位を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.receipt_import AS t (
    id,
    user_id,
    file_sha256,
    idempotency_key,
    status,
    revision,
    committed_at,
    reverted_at
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(file_sha256)s,
    %(idempotency_key)s,
    %(status)s,
    %(revision)s,
    %(committed_at)s,
    %(reverted_at)s
)
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
