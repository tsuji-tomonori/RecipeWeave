-- 工程別メディア選択を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_media AS t (
    id,
    step_id,
    media_id,
    start_ms,
    end_ms
)
VALUES (
    %(row_id)s,
    %(step_id)s,
    %(media_id)s,
    %(start_ms)s,
    %(end_ms)s
)
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.media_id,
    t.start_ms,
    t.end_ms,
    t.xmin::TEXT AS etag;
