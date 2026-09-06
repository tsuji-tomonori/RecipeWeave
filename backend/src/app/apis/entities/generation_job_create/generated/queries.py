# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    attempt_count: int
    error_code: str | None
    finished_at: datetime | None
    idempotency_key: str
    policy_id: UUID
    row_id: UUID
    seed: int | None
    started_at: datetime | None
    status: str


SQL = """-- 事前生成ジョブを作成する。
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
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "attempt_count": values["attempt_count"],
        "error_code": values["error_code"],
        "finished_at": values["finished_at"],
        "idempotency_key": values["idempotency_key"],
        "policy_id": values["policy_id"],
        "row_id": values["row_id"],
        "seed": values["seed"],
        "started_at": values["started_at"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
