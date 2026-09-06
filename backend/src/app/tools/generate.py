"""全操作のSQL呼出しとOpenAPIを決定的に生成し、書込みなしで差分を検出する。"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[4]
API = ROOT / "backend/src/app/apis"


def read_query(path: Path) -> str:
    """PostgreSQL文を解析し、複文・不明構文・曖昧な全列投影を拒否する。"""
    import sqlglot
    from sqlglot import exp

    text = path.read_text()
    if not text.lstrip().startswith("--"):
        raise ValueError(f"missing SQL processing summary: {path}")
    executable = re.sub(r"--[^\n]*", "", text).strip()
    if executable.upper().startswith("SET CONSTRAINTS"):
        from pglast import ast as postgres_ast
        from pglast import parse_sql

        parsed = parse_sql(text)
        if (
            len(parsed) != 1
            or not isinstance(parsed[0].stmt, postgres_ast.ConstraintsSetStmt)
            or parsed[0].stmt.constraints is not None
        ):
            raise ValueError(f"only one SET CONSTRAINTS ALL statement is supported: {path}")
        return text
    statements = sqlglot.parse(text, read="postgres")
    if len(statements) != 1 or statements[0] is None:
        raise ValueError(f"expected one SQL statement: {path}")
    if statements[0].find(exp.Star):
        raise ValueError(f"wildcard projection forbidden: {path}")
    if statements[0].find(exp.Command):
        raise ValueError(f"unsupported SQL statement: {path}")
    return text


def query_module(queries: dict[str, str]) -> str:
    """操作ごとの固定SQL集合を生成し、名前とパラメータの完全一致を実行時にも検査する。"""
    digest = hashlib.sha256("".join(queries.values()).encode()).hexdigest()
    literals = ",\n".join(f'    {name!r}: """\\\n{sql}"""' for name, sql in queries.items())
    parameters = {
        name: tuple(sorted(set(re.findall(r"%\((\w+)\)s", sql)))) for name, sql in queries.items()
    }
    return f'''# app-docs による自動生成。直接編集しない。
# SQLのSHA256: {digest}
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {{
{literals}
}}
PARAMETERS: dict[str, tuple[str, ...]] = {parameters!r}


def execute(connection: Connection[dict[str, Any]], name: str,
            params: Mapping[str, Any]) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []
'''


def single_module(sql: str) -> str:
    """カタログ用の単一SQLにも同じ名前・値の検査契約を適用する。"""
    source = query_module({"query": sql})
    source = source.replace("def execute(", "def _execute(")
    return (
        source
        + '''\n
SQL = QUERIES["query"]


def execute(connection: Connection[dict[str, Any]],
            values: Mapping[str, Any]) -> list[dict[str, Any]]:
    """固定した単文SQLを実行する。"""
    return _execute(connection, "query", values)
'''
    )


def generate_outputs(openapi_only: bool = False) -> dict[Path, str]:
    """実ルートのOpenAPIと、SQLを持つ全操作の呼出しを生成する。"""
    from app.main import create_app

    outputs = {
        ROOT / "backend/openapi.gen.json": json.dumps(
            create_app().openapi(), ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n"
    }
    if openapi_only:
        return outputs
    for directory in sorted(API.glob("*/*/sql")):
        queries = {path.stem: read_query(path) for path in sorted(directory.glob("*.sql"))}
        if not queries or directory.relative_to(API).parts[0] == "entities":
            continue
        generated = directory.parent / "generated"
        outputs[generated / "queries.py"] = query_module(queries)
        for name, sql in queries.items():
            module = "q" + name if name[0].isdigit() else name
            outputs[generated / f"{module}.py"] = single_module(sql)
    formatter = shutil.which("ruff")
    if formatter is None:
        raise RuntimeError("locked Ruff formatter is required")
    with TemporaryDirectory(prefix="app-docs-format-") as scratch:
        temporary = Path(scratch)
        targets = {
            path: temporary / path.relative_to(ROOT) for path in outputs if path.suffix == ".py"
        }
        for path, target in targets.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(outputs[path])
        subprocess.run(  # noqa: S603 -- 固定したRuffをシェルなしで起動する
            [
                formatter,
                "check",
                "--config",
                str(ROOT / "backend/pyproject.toml"),
                "--config",
                'lint.isort.known-first-party=["app"]',
                "--fix",
                str(temporary),
            ],
            capture_output=True,
            check=False,
        )
        subprocess.run(  # noqa: S603 -- 固定したRuffをシェルなしで起動する
            [formatter, "format", "--config", str(ROOT / "backend/pyproject.toml"), str(temporary)],
            capture_output=True,
            check=True,
        )
        for path, target in targets.items():
            outputs[path] = target.read_text()
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--openapi-only", action="store_true")
    args = parser.parse_args()
    outputs = generate_outputs(openapi_only=args.openapi_only)
    stale: list[str] = []
    for path, text in outputs.items():
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise ValueError(f"symlink output forbidden: {path}")
        if not path.is_file() or path.read_text() != text:
            if args.check:
                stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                temporary = path.with_suffix(path.suffix + ".tmp")
                temporary.write_text(text)
                temporary.replace(path)
    if stale:
        print("Generated drift: " + ", ".join(stale))
        return 1
    print("SQL wrappers and OpenAPI are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
