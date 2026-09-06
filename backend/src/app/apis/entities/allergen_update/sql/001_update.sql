-- アレルゲン概念を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.allergen AS t
SET
    code = %(code)s,
    name = %(name)s,
    source_id = %(source_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.source_id,
    t.xmin::TEXT AS etag;
