-- 検索・キャッシュ更新配信を取得する。
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
    t.id = %(row_id)s
    AND TRUE;
