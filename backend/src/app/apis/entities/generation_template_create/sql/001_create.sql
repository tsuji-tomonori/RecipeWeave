-- 列挙テンプレート版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_template AS t (
    id,
    code,
    version,
    release_id,
    contract,
    candidate_count,
    contract_hash
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(version)s,
    %(release_id)s,
    %(contract)s,
    %(candidate_count)s,
    %(contract_hash)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.version,
    t.release_id,
    t.contract,
    t.candidate_count,
    t.contract_hash,
    t.xmin::TEXT AS etag;
