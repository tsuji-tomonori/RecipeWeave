-- アプリ利用者を一覧取得する。
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
    t.id = %(actor_id)s
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
