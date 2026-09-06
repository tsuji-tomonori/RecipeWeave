-- 組み合わせ軸を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.purpose,
    t.selection,
    t.release_id,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.axis AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
