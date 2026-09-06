-- 検索・キャッシュ更新配信を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.event_type,
    t.aggregate_id,
    t.payload,
    t.delivered_at,
    t.attempt_count,
    t.xmin::TEXT AS etag
FROM recipeweave.outbox_event AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
