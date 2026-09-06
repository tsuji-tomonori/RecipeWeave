"""生成済みの操作別クエリだけを、固定操作名と固定ファイル名で呼び出す。"""

from collections.abc import Mapping
from importlib import import_module
from typing import Any, Protocol, cast

from psycopg import Connection


class Query(Protocol):
    def __call__(
        self, connection: Connection[dict[str, Any]], values: Mapping[str, Any]
    ) -> list[dict[str, Any]]: ...


class OperationQueries:
    """操作名・SQL名は呼び出し元の定数からのみ指定し、HTTP入力を使わない。"""

    def __init__(self, connection: Connection[dict[str, Any]], operation: str) -> None:
        self.connection = connection
        self.operation = operation

    def run(self, query_name: str, **values: Any) -> list[dict[str, Any]]:
        """SQLファイルから生成した型付きラッパーへ束縛値を渡す。"""
        slug = self.operation.replace("/", ".")
        module = import_module(f"app.apis.{slug}.generated.{query_name}")
        execute = cast(Query, module.execute)
        return execute(self.connection, values)
