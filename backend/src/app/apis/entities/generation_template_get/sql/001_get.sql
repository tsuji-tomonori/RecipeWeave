-- 列挙テンプレート版を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.version,
    t.release_id,
    t.contract,
    t.candidate_count,
    t.contract_hash,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_template AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
