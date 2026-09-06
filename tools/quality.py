"""関連する品質ゲートを省略せず実行し、終了コードとログを逐次保存する。"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UV = ["uv", "run", "--locked"]


def checks() -> list[tuple[str, list[str]]]:
    """型・SQL・実DB・単体・生成差分を独立した検査として公開する。"""
    return [
        (
            "Ruff整形",
            UV
            + [
                "ruff",
                "format",
                "--check",
                "backend",
                "database",
                "tools/design",
                "tools/quality.py",
                "tools/local_database.py",
                "tools/start_database.py",
                "tools/require_executed_tests.py",
                "tools/verified_revision.py",
                "tools/wait_services.py",
                "tools/deployment_readiness.py",
                "tools/prepare_e2e_database.py",
            ],
        ),
        (
            "Ruff静的解析",
            UV
            + [
                "ruff",
                "check",
                "backend",
                "database",
                "packages/generator",
                "tools/design",
                "tools/quality.py",
                "tools/local_database.py",
                "tools/start_database.py",
                "tools/require_executed_tests.py",
                "tools/verified_revision.py",
                "tools/wait_services.py",
                "tools/deployment_readiness.py",
                "tools/prepare_e2e_database.py",
            ],
        ),
        ("SQLFluff・SQL構造", UV + ["--package", "recipeweave-api", "app-sql-lint"]),
        ("API構造", UV + ["--package", "recipeweave-api", "app-archlint"]),
        ("Pyright strict", UV + ["pyright", "--project", "backend/pyproject.toml"]),
        (
            "mypy strict",
            UV
            + [
                "mypy",
                "--config-file",
                "backend/pyproject.toml",
                "backend/src",
                "backend/tests",
                "backend/tools",
                "database",
            ],
        ),
        ("フロントエンド型検査", ["npm", "--prefix", "frontend", "run", "check"]),
        (
            "Vitest単体試験",
            [
                "npm",
                "--prefix",
                "frontend",
                "test",
                "--",
                "--coverage",
                "--reporter=default",
                "--reporter=json",
                "--outputFile=../reports/vitest.json",
            ],
        ),
        (
            "pytest単体・実DB統合",
            UV
            + [
                "pytest",
                "packages/generator/tests",
                "backend/tests",
                "tests",
                "--cov=app",
                "--cov=recipeweave_generator",
                "--cov-branch",
                "--cov-report=term-missing",
                "--cov-report=json:reports/python-coverage.json",
                "--cov-report=html:reports/python-coverage",
                "--junitxml=reports/python-junit.xml",
                "-q",
            ],
        ),
        (
            "必須試験の実行証跡",
            UV + ["python", "tools/require_executed_tests.py", "reports/python-junit.xml"],
        ),
        ("CDK厳密な型検査", ["npm", "--prefix", "infra", "run", "typecheck"]),
        ("CDK静的解析", ["npm", "--prefix", "infra", "run", "lint"]),
        ("CDK構造試験", ["npm", "--prefix", "infra", "run", "test:evidence"]),
        ("Quint正本", UV + ["python", "tools/quintflow.py", "check"]),
        ("API・SQL生成差分", UV + ["--package", "recipeweave-api", "app-docs", "--check"]),
        ("設計書再生成の決定性", UV + ["python", "tools/generate_service_design.py", "--check"]),
        ("図の構文", ["node", "tools/docs_diagrams.mjs"]),
    ]


def main() -> int:
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    results: list[dict[str, object]] = []
    for name, command in checks():
        print(name, flush=True)
        try:
            result = subprocess.run(
                command,
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                timeout=900,
            )
            code, output = result.returncode, result.stdout
        except (OSError, subprocess.TimeoutExpired) as error:
            code, output = 1, str(error)
        results.append({"name": name, "command": command, "exit_code": code, "output": output})
        (reports / "quality.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2) + "\n"
        )
        print(output[-2500:], flush=True)
    return int(any(item["exit_code"] for item in results))


if __name__ == "__main__":
    sys.exit(main())
