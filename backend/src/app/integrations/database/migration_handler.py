"""専用LambdaでPostgreSQL移行と非管理者ロール設定を実行する。"""

import os

import psycopg
from database.migrate import apply_migrations, load_migrations
from psycopg import sql

from app.core.settings import AppSettings
from app.integrations.database.aws_provider import connection_kwargs, read_credentials


def handler(event: dict[str, object], context: object) -> dict[str, str]:
    """移行専用IAMロールだけが管理secretを読み取る。試験用データは自動投入しない。"""
    del context
    if event:
        raise ValueError("移行関数は空の要求だけを受け付けます")
    settings = AppSettings()
    with psycopg.connect(**connection_kwargs(settings), autocommit=True) as connection:
        connection.execute("SELECT pg_advisory_lock(782345611)")
        try:
            apply_migrations(connection, load_migrations())
            username, password = read_credentials(
                os.environ["APPLICATION_DATABASE_SECRET_ARN"], settings.aws_region
            )
            if username != "recipeweave_app":
                raise ValueError("アプリ用DBロール名が一致しません")
            exists = connection.execute(
                "SELECT 1 FROM pg_roles WHERE rolname = %s", (username,)
            ).fetchone()
            if exists is None:
                connection.execute("CREATE ROLE recipeweave_app LOGIN NOSUPERUSER NOBYPASSRLS")
            connection.execute(
                sql.SQL("ALTER ROLE recipeweave_app NOSUPERUSER NOBYPASSRLS PASSWORD {}").format(
                    sql.Literal(password)
                )
            )
            connection.execute("GRANT USAGE ON SCHEMA recipeweave TO recipeweave_app")
            connection.execute(
                "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA recipeweave "
                "TO recipeweave_app"
            )
            connection.execute(
                "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA recipeweave TO recipeweave_app"
            )
            connection.execute("REVOKE ALL ON recipeweave.schema_migrations FROM recipeweave_app")
        finally:
            connection.execute("SELECT pg_advisory_unlock(782345611)")
    return {"status": "migrated"}
