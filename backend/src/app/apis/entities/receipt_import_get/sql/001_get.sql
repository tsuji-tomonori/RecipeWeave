-- レシート読取・在庫登録の処理単位を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.file_sha256,
    t.idempotency_key,
    t.status,
    t.revision,
    t.committed_at,
    t.reverted_at,
    t.undo_preserved_count,
    t.xmin::TEXT AS etag
FROM recipeweave.receipt_import AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
