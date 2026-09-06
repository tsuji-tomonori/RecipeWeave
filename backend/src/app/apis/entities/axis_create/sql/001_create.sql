-- 組み合わせ軸を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.axis AS t (
    id,
    code,
    name,
    purpose,
    selection,
    release_id,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(purpose)s,
    %(selection)s,
    %(release_id)s,
    %(status)s
)
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
