-- アプリ利用者を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.app_user AS t
SET
    locale = %(locale)s,
    timezone = %(timezone)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.auth_subject,
    t.state,
    t.locale,
    t.timezone,
    t.xmin::TEXT AS etag;
