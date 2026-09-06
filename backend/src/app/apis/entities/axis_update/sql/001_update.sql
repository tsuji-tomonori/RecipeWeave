-- 組み合わせ軸を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.axis AS t
SET
    code = %(code)s,
    name = %(name)s,
    purpose = %(purpose)s,
    selection = %(selection)s,
    release_id = %(release_id)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.purpose,
    t.selection,
    t.release_id,
    t.status,
    t.xmin::TEXT AS etag;
