-- 事前生成ジョブを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.policy_id,
    t.idempotency_key,
    t.status,
    t.started_at,
    t.finished_at,
    t.seed,
    t.error_code,
    t.attempt_count,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_job AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
