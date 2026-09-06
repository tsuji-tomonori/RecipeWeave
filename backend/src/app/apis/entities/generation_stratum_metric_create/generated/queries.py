# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    attempted: int
    cost_amount: Decimal | None
    currency: str | None
    input_tokens: int
    output_tokens: int
    publishable: int
    row_id: UUID
    stratum_key: str
    template_id: UUID
    unique_count: int
    valid: int
    window_end: datetime
    window_start: datetime


SQL = """-- 採用率・飽和度の実測を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_stratum_metric AS t (
    id,
    template_id,
    window_start,
    window_end,
    attempted,
    valid,
    unique_count,
    publishable,
    input_tokens,
    output_tokens,
    cost_amount,
    currency,
    stratum_key
)
VALUES (
    %(row_id)s,
    %(template_id)s,
    %(window_start)s,
    %(window_end)s,
    %(attempted)s,
    %(valid)s,
    %(unique_count)s,
    %(publishable)s,
    %(input_tokens)s,
    %(output_tokens)s,
    %(cost_amount)s,
    %(currency)s,
    %(stratum_key)s
)
RETURNING
    t.id,
    t.created_at,
    t.template_id,
    t.window_start,
    t.window_end,
    t.attempted,
    t.valid,
    t.unique_count,
    t.publishable,
    t.input_tokens,
    t.output_tokens,
    t.cost_amount,
    t.currency,
    t.stratum_key,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "attempted": values["attempted"],
        "cost_amount": values["cost_amount"],
        "currency": values["currency"],
        "input_tokens": values["input_tokens"],
        "output_tokens": values["output_tokens"],
        "publishable": values["publishable"],
        "row_id": values["row_id"],
        "stratum_key": values["stratum_key"],
        "template_id": values["template_id"],
        "unique_count": values["unique_count"],
        "valid": values["valid"],
        "window_end": values["window_end"],
        "window_start": values["window_start"],
    }
    return list(connection.execute(SQL, params).fetchall())
