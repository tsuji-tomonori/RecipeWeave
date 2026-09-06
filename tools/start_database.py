"""ローカル環境の移行・最小権限ロール・初期データを順番に設定する。"""

import os
import subprocess
import sys


def main() -> None:
    environment = dict(os.environ)
    environment["DATABASE_URL"] = environment["MIGRATION_DATABASE_URL"]
    subprocess.run([sys.executable, "database/migrate.py", "--apply"], env=environment, check=True)
    subprocess.run([sys.executable, "tools/local_database.py"], check=True)
    subprocess.run([sys.executable, "-m", "database.seed"], check=True)


if __name__ == "__main__":
    main()
