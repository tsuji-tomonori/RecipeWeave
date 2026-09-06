-- アプリ利用者を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.auth_subject,
    t.state,
    t.locale,
    t.timezone,
    t.xmin::TEXT AS etag
FROM recipeweave.app_user AS t
WHERE
    t.id = %(row_id)s
    AND t.id = %(actor_id)s;
