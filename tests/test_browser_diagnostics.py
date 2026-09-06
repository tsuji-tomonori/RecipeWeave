"""CI診断から認証情報が漏れず、障害を調べる状態は残ることを検証する。"""

from pathlib import Path

import pytest

from tools.browser_diagnostics import read_safe, sanitize


def test_authentication_values_and_database_urls_are_removed() -> None:
    value = "\n".join(
        [
            "INFO GET /api/workspace 500 Internal Server Error",
            "Authorization: Bearer private-session",
            "LOCAL_AUTH_SECRET: a-private-secret",
            'textbox "パスワード": private-password',
            "postgresql://owner:private-db@127.0.0.1:5432/recipeweave",
            "opaque eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyIn0.signature",
            "https://example.test/?code=private-code&state=private-state",
        ]
    )
    result = sanitize(value)
    assert "GET /api/workspace 500" in result
    assert "private-" not in result
    assert "eyJ" not in result
    assert "owner:" not in result


def test_allowed_failure_context_is_bounded_and_readable(tmp_path: Path) -> None:
    path = tmp_path / "error-context.md"
    path.write_text("x" * 200 + "\nheading 接続に失敗しました")
    result = read_safe(path, tmp_path, 100)
    assert "末尾のみ" in result
    assert "接続に失敗しました" in result
    assert len(result.encode()) < 200


def test_evidence_symlink_is_not_followed(tmp_path: Path) -> None:
    allowed = tmp_path / "evidence"
    allowed.mkdir()
    source = tmp_path / "outside.txt"
    source.write_text("private file")
    link = allowed / "error-context.md"
    link.symlink_to(source)
    with pytest.raises(ValueError, match="パス"):
        read_safe(link, allowed, 1000)
