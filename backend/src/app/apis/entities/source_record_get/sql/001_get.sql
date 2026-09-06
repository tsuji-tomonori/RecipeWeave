-- 根拠資料を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.title,
    t.url,
    t.locator,
    t.retrieved_at,
    t.content_hash,
    t.license_note,
    t.xmin::TEXT AS etag
FROM recipeweave.source_record AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
