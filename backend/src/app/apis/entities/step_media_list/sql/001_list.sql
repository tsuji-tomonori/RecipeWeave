-- 工程別メディア選択を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.step_id,
    t.media_id,
    t.start_ms,
    t.end_ms,
    t.xmin::TEXT AS etag
FROM recipeweave.step_media AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
