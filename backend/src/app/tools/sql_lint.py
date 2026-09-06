"""API別SQLと移行定義を、実行せずにSQLFluffで静的解析する。"""

import json
import subprocess
import sys
from pathlib import Path

from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[4]


class VerificationSource(BaseModel):
    """移行マニフェストから構文検査に必要な情報だけを読む。"""

    id: str
    verify: str


class VerificationManifest(BaseModel):
    """移行の完全な契約検査は database/migrate.py が担当する。"""

    migrations: list[VerificationSource]


def run_sqlfluff(
    arguments: list[str], *, source: str | None = None, root: Path = ROOT
) -> subprocess.CompletedProcess[str]:
    """固定環境のSQLFluffへSQL定義だけを渡す。接続情報や実行値は使用しない。"""
    return subprocess.run(  # noqa: S603 -- 実行対象は固定したPythonモジュールで、シェルを使用しない
        [
            sys.executable,
            "-m",
            "sqlfluff",
            *arguments,
            "--ignore-local-config",
            "--config",
            str(root / ".sqlfluff"),
        ],
        input=source,
        text=True,
        capture_output=True,
        cwd=root,
        timeout=60,
        check=False,
    )


def inspect_sql(root: Path = ROOT) -> list[str]:
    """全APIのSQLファイルと移行SQLを検査し、既存移行のバイト列は変更しない。"""
    api_root = root / "backend/src/app/apis"
    migration_root = root / "database/migrations"
    api_sql = sorted(api_root.rglob("*.sql"))
    migration_sql = sorted(migration_root.glob("*.sql"))
    errors = [
        f"API別の sql ディレクトリ外にSQLがあります: {path.relative_to(root)}"
        for path in api_sql
        if path.parent.name != "sql" or not (path.parent.parent / "contract.py").is_file()
    ]
    if not api_sql or not migration_sql:
        errors.append("検査対象のAPI SQLまたは移行SQLが見つかりません。")
        return errors
    result = run_sqlfluff(["lint", *[str(path) for path in [*api_sql, *migration_sql]]], root=root)
    if result.returncode:
        errors.append(result.stdout + result.stderr)

    manifest = VerificationManifest.model_validate_json(
        (migration_root / "manifest.manual.json").read_text()
    )
    for migration in manifest.migrations:
        # 確定済み移行は検証SQLもチェックサムに含むため、再整形せず構文だけを検査する。
        parsed = run_sqlfluff(
            ["parse", "--format", "json", "-"], source=migration.verify, root=root
        )
        if parsed.returncode:
            errors.append(f"移行後検証SQLの構文エラー: {migration.id}\n{parsed.stderr}")
            continue
        if not json.loads(parsed.stdout):
            errors.append(f"移行後検証SQLを解析できませんでした: {migration.id}")
    return errors


def main() -> int:
    errors = inspect_sql()
    if errors:
        print("\n".join(errors))
        return 1
    print("API別SQL・移行SQLの規約と、移行後検証SQLの構文は正常です。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
