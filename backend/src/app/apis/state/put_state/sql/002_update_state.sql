-- 期待した版と一致する本人の保存状態だけを置換し、新しい版を返す。
UPDATE recipeweave.user_state
SET
    revision = revision + 1,
    payload = %(payload)s,
    updated_at = CURRENT_TIMESTAMP
WHERE subject = %(subject)s AND revision = %(revision)s
RETURNING revision;
