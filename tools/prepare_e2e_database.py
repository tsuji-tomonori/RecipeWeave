"""単体試験がコミットした業務データを、ブラウザE2Eの初期状態へ混ぜない。"""

import os
import subprocess
import sys
from urllib.parse import urlsplit

import psycopg


def main() -> None:
    if os.environ.get("ENVIRONMENT") != "test":
        raise SystemExit("E2E専用DBの準備はENVIRONMENT=testだけで実行できます")
    original = os.environ["MIGRATION_DATABASE_URL"]
    with psycopg.connect(original, autocommit=True) as connection:
        # 既存DBを消して再利用せず、意図しない再実行はエラーとして止める。
        connection.execute("CREATE DATABASE recipeweave_e2e")
    environment = dict(os.environ)
    environment["MIGRATION_DATABASE_URL"] = (
        urlsplit(original)._replace(path="/recipeweave_e2e").geturl()
    )
    environment["DATABASE_URL"] = (
        urlsplit(environment["DATABASE_URL"])._replace(path="/recipeweave_e2e").geturl()
    )
    subprocess.run([sys.executable, "tools/start_database.py"], env=environment, check=True)
    print("E2E専用の実DBを同じ移行・初期データで準備しました")


if __name__ == "__main__":
    main()
