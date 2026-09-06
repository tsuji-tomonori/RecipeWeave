"""配備証跡と必須試験の未実行が成功に読み替えられないことを確認する。"""

from pathlib import Path

import pytest

from tools.require_executed_tests import verify
from tools.verified_revision import matches


def test_only_exact_source_commit_and_tree_are_accepted() -> None:
    source, commit, tree = "a" * 40, "b" * 40, "c" * 40
    assert matches(f"{source}\n{commit}\n{tree}\n", source=source, commit=commit, tree=tree)
    assert not matches(f"{source}\n{commit}\n{'d' * 40}\n", source=source, commit=commit, tree=tree)
    assert not matches(
        f"{source}\n{commit}\n{tree}\nextra", source=source, commit=commit, tree=tree
    )


@pytest.mark.parametrize(
    "case", ["", "<testcase><skipped/></testcase>", "<testcase><failure/></testcase>"]
)
def test_missing_or_failed_required_database_test_is_rejected(tmp_path: Path, case: str) -> None:
    path = tmp_path / "junit.xml"
    path.write_text(f"<testsuites><testsuite>{case}</testsuite></testsuites>")
    with pytest.raises(ValueError):
        verify(path)


def test_executed_database_test_is_accepted(tmp_path: Path) -> None:
    path = tmp_path / "junit.xml"
    path.write_text('<testsuites><testsuite><testcase name="実DB"/></testsuite></testsuites>')
    verify(path)
