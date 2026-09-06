-- 再送キーと登録時刻を一度だけ確定する。画像本文は保持しない。
INSERT INTO recipeweave.receipt_import (
    id, user_id, file_sha256, idempotency_key, status, committed_at
)
VALUES (%(import_id)s, %(user_id)s, %(hash)s, %(key)s, 'committed', CURRENT_TIMESTAMP);
