-- 認証済み本人の現在の版と保存状態だけを取得する。
SELECT
    revision,
    payload
FROM recipeweave.user_state
WHERE subject = %(subject)s;
