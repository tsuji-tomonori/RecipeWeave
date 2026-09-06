-- 根拠資料を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.source_record AS t (
    id,
    title,
    url,
    locator,
    retrieved_at,
    content_hash,
    license_note
)
VALUES (
    %(row_id)s,
    %(title)s,
    %(url)s,
    %(locator)s,
    %(retrieved_at)s,
    %(content_hash)s,
    %(license_note)s
)
RETURNING
    t.id,
    t.created_at,
    t.title,
    t.url,
    t.locator,
    t.retrieved_at,
    t.content_hash,
    t.license_note,
    t.xmin::TEXT AS etag;
