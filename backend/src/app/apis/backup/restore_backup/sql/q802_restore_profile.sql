-- 本人の言語とタイムゾーンだけを復元し、認証主体とアカウント状態は保持する。
UPDATE recipeweave.app_user SET locale = %(locale)s, timezone = %(timezone)s
WHERE id = %(actor_id)s;
