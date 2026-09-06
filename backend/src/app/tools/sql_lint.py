"""API別SQLと移行定義を、実行せずにSQLFluffで静的解析する。"""

import json
import os
import subprocess
import sys
from pathlib import Path

from pydantic import BaseModel, TypeAdapter

ROOT = Path(__file__).resolve().parents[4]


class SqlDiagnostic(BaseModel):
    """SQL本文や実行値を含めず、ファイルと静的な違反位置を保存する。"""

    filepath: str
    violations: list[dict[str, object]]


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
        timeout=300,
        check=False,
    )


def inspect_sql(root: Path = ROOT, *, evidence: Path | None = None) -> list[str]:
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
    shared_sql = sorted((root / "backend/src/app/entities/sql").glob("*.sql"))
    result = run_sqlfluff(
        [
            "lint",
            "--processes",
            "4",
            "--disable-progress-bar",
            "--format",
            "json",
            *[str(path) for path in [*api_sql, *shared_sql, *migration_sql]],
        ],
        root=root,
    )
    diagnostics = TypeAdapter(list[SqlDiagnostic]).validate_json(result.stdout)
    if evidence is not None:
        if not evidence.resolve().is_relative_to((root / "reports").resolve()):
            raise ValueError("SQLFluffの証跡はreports配下だけに保存できます")
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(
            json.dumps([item.model_dump() for item in diagnostics], ensure_ascii=False, indent=2)
            + "\n"
        )
    if result.returncode:
        for item in diagnostics:
            for violation in item.violations:
                errors.append(
                    f"{item.filepath}:{violation.get('start_line_no', '?')}: "
                    f"{violation.get('code', '?')} {violation.get('description', '')}"
                )
        if result.stderr:
            errors.append(result.stderr[-2000:])

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
    output = os.environ.get("SQLFLUFF_OUTPUT")
    errors = inspect_sql(evidence=ROOT / output if output else None)
    if errors:
        print("\n".join(errors))
        return 1
    print("API別SQL・移行SQLの規約と、移行後検証SQLの構文は正常です。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
