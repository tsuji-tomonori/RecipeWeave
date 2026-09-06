-- 事前生成ジョブを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_job AS t (
    id,
    policy_id,
    idempotency_key,
    status,
    started_at,
    finished_at,
    seed,
    error_code,
    attempt_count
)
VALUES (
    %(row_id)s,
    %(policy_id)s,
    %(idempotency_key)s,
    %(status)s,
    %(started_at)s,
    %(finished_at)s,
    %(seed)s,
    %(error_code)s,
    %(attempt_count)s
)
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
