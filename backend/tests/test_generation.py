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
