-- 検証済みバックアップのレシート読取・在庫登録の処理単位を元IDと全列で復元する。
INSERT INTO recipeweave.receipt_import (
    id,
    created_at,
    user_id,
    file_sha256,
    idempotency_key,
    status,
    revision,
    committed_at,
    reverted_at,
    undo_preserved_count
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(file_sha256)s,
    %(idempotency_key)s,
    %(status)s,
    %(revision)s,
    %(committed_at)s,
    %(reverted_at)s,
    %(undo_preserved_count)s
);
