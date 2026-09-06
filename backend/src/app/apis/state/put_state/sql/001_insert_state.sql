-- 最初の版を作成する。同時に作成された場合は版の競合として扱う。
INSERT INTO recipeweave.user_state (subject, revision, payload, updated_at)
VALUES (%(subject)s, 1, %(payload)s, CURRENT_TIMESTAMP);
