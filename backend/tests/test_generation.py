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
