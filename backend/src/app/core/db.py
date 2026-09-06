"""API要求ごとにPostgreSQL接続とトランザクションを一つ構築する。"""

from collections.abc import Iterator
from typing import Annotated, Any

import psycopg
from fastapi import Depends
from psycopg.rows import dict_row

from app.core.dependencies import get_settings
from app.core.errors import ServiceUnavailableError


def get_database() -> Iterator[psycopg.Connection[dict[str, Any]]]:
    """正常応答のみコミットし、認証・制約・処理の失敗はすべてロールバックする。"""
    settings = get_settings()
    if not settings.database_url and not settings.database_secret_arn:
        raise ServiceUnavailableError("データベース接続が設定されていません")
    kwargs: dict[str, str] = {}
    if not settings.database_url:
        from app.integrations.database.aws_provider import connection_kwargs

        options = connection_kwargs(settings)
        kwargs = {
            "host": options["host"],
            "dbname": options["dbname"],
            "user": options["user"],
            "password": options["password"],
            "sslmode": options["sslmode"],
        }
    try:
        with psycopg.Connection[dict[str, Any]].connect(
            settings.database_url,
            row_factory=dict_row,
            connect_timeout=5,
            options="-c search_path=recipeweave,public -c statement_timeout=15000",
            host=kwargs.get("host"),
            dbname=kwargs.get("dbname"),
            user=kwargs.get("user"),
            password=kwargs.get("password"),
            sslmode=kwargs.get("sslmode"),
        ) as connection:
            yield connection
    except psycopg.OperationalError as exc:
        raise ServiceUnavailableError("データベースに接続できません") from exc


DatabaseDependency = Annotated[
    psycopg.Connection[dict[str, Any]], Depends(get_database, scope="function")
]
