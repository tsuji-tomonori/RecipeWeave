"""ローカル・CI専用の非管理者DBロールを用意し、RLSの迂回を防ぐ。"""

import os

import psycopg
from psycopg import sql


def main() -> None:
    if os.environ.get("ENVIRONMENT") not in {"local", "test"}:
        raise SystemExit("この初期化はENVIRONMENT=local/test専用です")
    with psycopg.connect(os.environ["MIGRATION_DATABASE_URL"], autocommit=True) as connection:
        exists = connection.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s", ("recipeweave_app",)
        ).fetchone()
        if exists is None:
            connection.execute("CREATE ROLE recipeweave_app LOGIN NOSUPERUSER NOBYPASSRLS")
        connection.execute(
            sql.SQL("ALTER ROLE recipeweave_app WITH NOSUPERUSER NOBYPASSRLS PASSWORD {}").format(
                sql.Literal("recipeweave-local")
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
    with psycopg.connect(os.environ["DATABASE_URL"]) as connection:
        flags = connection.execute(
            "SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user"
        ).fetchone()
        if flags != (False, False):
            raise SystemExit("アプリロールでのRLS迂回を拒否しました")
    print("アプリロールのNOSUPERUSER/NOBYPASSRLSを確認しました")


if __name__ == "__main__":
    main()
