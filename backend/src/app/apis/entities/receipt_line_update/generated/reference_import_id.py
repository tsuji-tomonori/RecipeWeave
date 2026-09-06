# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    reference_id: UUID


SQL = """-- 参照先のレシート読取・在庫登録の処理単位が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.receipt_import AS t
WHERE
    t.id = %(reference_id)s
    AND t.user_id = %(actor_id)s;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"actor_id": values["actor_id"], "reference_id": values["reference_id"]}
    return list(connection.execute(SQL, params).fetchall())
