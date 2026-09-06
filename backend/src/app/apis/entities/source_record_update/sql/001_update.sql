-- 根拠資料を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.source_record AS t
SET
    title = %(title)s,
    url = %(url)s,
    locator = %(locator)s,
    retrieved_at = %(retrieved_at)s,
    content_hash = %(content_hash)s,
    license_note = %(license_note)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
