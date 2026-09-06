import ast
from pathlib import Path

import pytest

from app.tools.archlint import inspect_operations


def test_operation_architecture_contracts() -> None:
    assert inspect_operations() == []


def test_codegen_is_deterministic_and_rejects_wildcards(tmp_path: Path) -> None:
    pytest.importorskip("sqlglot", reason="locked SQL parser must be installed for generation")
    from app.tools.generate import generate_outputs, read_query

    assert generate_outputs() == generate_outputs()
    source = tmp_path / "bad.sql"
    source.write_text("-- 禁止されたワイルドカード\nSELECT * FROM example;\n")
    with pytest.raises(ValueError, match="wildcard"):
        read_query(source)
    source.write_text("-- 禁止された複数文\nSELECT x FROM example; DELETE FROM example;\n")
    with pytest.raises(ValueError, match="one SQL"):
        read_query(source)


def test_long_japanese_sql_comment_preserves_bytes_without_long_python_line() -> None:
    """SQL本文を変えず、長い操作名と日本語説明を別行へ生成する。"""
    from app.tools.generate import query_module

    name = "q005_initialize_internal_resource"
    sql = "-- 初回ログイン時の作業枠だけを作り、利用者が選ぶ可視器具は追加しない。\nSELECT 1;\n"
    generated = query_module({name: sql})
    declaration = next(
        node
        for node in ast.parse(generated).body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == "QUERIES"
    )
    assert declaration.value is not None
    assert ast.literal_eval(declaration.value) == {name: sql}
    assert all(len(line) <= 100 for line in generated.splitlines())


@pytest.mark.parametrize("table_name", ["backup_artifact", "backup_restore_intent"])
@pytest.mark.parametrize("action", ["get", "list"])
def test_entity_long_description_keeps_sql_and_tags_after_formatting(
    tmp_path: Path, table_name: str, action: str
) -> None:
    """長い日本語説明を全角の表示桁数で折返し、SQLとAPIタグの内容を保持する。"""
    import subprocess

    from tools.generate_entity_apis import load_tables, operation_files

    root = Path(__file__).resolve().parents[2]
    tables = {table["name"]: table for table in load_tables()}
    files, _ = operation_files(tables[table_name], action, tables)
    generated = {
        name: next(text for path, text in files.items() if path.name == name)
        for name in ("router.py", "queries.py")
    }
    sql = next(text for path, text in files.items() if path.name == "001_" + action + ".sql")
    for name, text in generated.items():
        (tmp_path / name).write_text(text)
    (tmp_path / "base").mkdir()
    (tmp_path / "base/pyproject.toml").write_text((root / "pyproject.toml").read_text())
    (tmp_path / "pyproject.toml").write_text(
        (root / "backend/pyproject.toml")
        .read_text()
        .replace("../pyproject.toml", "base/pyproject.toml")
    )
    subprocess.run(
        ["/usr/bin/env", "ruff", "format", "."],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    checked = subprocess.run(
        ["/usr/bin/env", "ruff", "check", "--select", "E501", "."],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert checked.returncode == 0, checked.stdout
    query_tree = ast.parse((tmp_path / "queries.py").read_text())
    sql_assignment = next(
        node
        for node in query_tree.body
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "SQL"
    )
    assert ast.literal_eval(sql_assignment.value) == sql
    router_tree = ast.parse((tmp_path / "router.py").read_text())
    router = next(
        node.value
        for node in router_tree.body
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "router"
        and isinstance(node.value, ast.Call)
    )
    tags = next(keyword.value for keyword in router.keywords if keyword.arg == "tags")
    assert ast.literal_eval(tags) == ["正規化データ: " + tables[table_name]["description"]]
