-- 生成軸の選択値を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_choice AS t (
    id,
    job_id,
    option_id
)
VALUES (
    %(row_id)s,
    %(job_id)s,
    %(option_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.job_id,
    t.option_id,
    t.xmin::TEXT AS etag;
