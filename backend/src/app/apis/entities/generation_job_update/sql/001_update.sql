-- 事前生成ジョブを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.generation_job AS t
SET
    policy_id = %(policy_id)s,
    idempotency_key = %(idempotency_key)s,
    status = %(status)s,
    started_at = %(started_at)s,
    finished_at = %(finished_at)s,
    seed = %(seed)s,
    error_code = %(error_code)s,
    attempt_count = %(attempt_count)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
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
    t.xmin::TEXT AS etag;
