"""テーブル操作の固定メタデータとSQL実行境界。"""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Literal

from psycopg import Connection

Action = Literal["list", "get", "create", "update", "delete"]
Row = dict[str, Any]
Query = Callable[[Connection[Row], Mapping[str, Any]], list[Row]]


@dataclass(frozen=True)
class OperationSpec:
    """外部入力で変更できない、生成時に確定した操作契約。"""

    operation_id: str
    table: str
    action: Action
    owned: bool
    input_columns: tuple[str, ...]
    json_columns: tuple[str, ...]
    bigint_columns: tuple[str, ...]
    reference_queries: tuple[tuple[str, Query], ...]
    query: Query
    immutable: bool = False
