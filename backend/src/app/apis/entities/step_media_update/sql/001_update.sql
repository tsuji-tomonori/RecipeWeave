-- 工程別メディア選択を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.step_media AS t
SET
    step_id = %(step_id)s,
    media_id = %(media_id)s,
    start_ms = %(start_ms)s,
    end_ms = %(end_ms)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.media_id,
    t.start_ms,
    t.end_ms,
    t.xmin::TEXT AS etag;
