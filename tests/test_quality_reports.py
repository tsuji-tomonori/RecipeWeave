"""証跡の欠落を成功扱いせず、画像と実テスト結果を公開できることを検査する。"""

import struct
import zlib
from pathlib import Path

import pytest

from tools.docs_site import prepare, slug, verify_html
from tools.report import collect_cases, generate
from tools.test_results import test_results as collect_test_results


def playwright_result(path: str | None = None) -> dict:
    return {
        "suites": [
            {
                "title": "冷蔵庫",
                "specs": [
                    {
                        "title": "食材を保存する",
                        "tests": [
                            {
                                "projectName": "mobile",
                                "results": [
                                    {
                                        "status": "passed",
                                        "attachments": [
                                            {
                                                "name": phase + ": 食材の状態を確認",
                                                "contentType": "image/png",
                                                "path": path,
                                            }
                                            for phase in ("Given", "When", "Then")
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }


def test_success_without_screenshots_is_missing_evidence(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    cases, count = collect_cases(playwright_result(), tmp_path, reports)
    assert count == 0
    assert cases[0]["status"] == "missing"
    assert "成功ケース" in cases[0]["errors"][-1]


def test_png_evidence_retains_all_three_phases(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    frontend = tmp_path / "frontend"
    frontend.mkdir()
    path = frontend / "step.png"

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", zlib.crc32(kind + payload))
        )

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 256, 512, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress((b"\0" + b"\0" * 1024) * 512))
        + chunk(b"IEND", b"")
    )
    cases, count = collect_cases(playwright_result(str(path)), tmp_path, reports)
    assert count == 3
    assert cases[0]["status"] == "passed"
    assert [step["kind"] for step in cases[0]["steps"]] == ["Given", "When", "Then"]
    assert cases[0]["steps"][0]["dimensions"] == (256, 512)


def test_evidence_outside_repository_is_rejected(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    with pytest.raises(ValueError, match="リポジトリ外"):
        collect_cases(playwright_result(str(tmp_path.parent / "secret.png")), tmp_path, reports)


def test_unexecuted_reports_show_pending_instead_of_success(tmp_path: Path) -> None:
    assert generate(tmp_path)
    text = (tmp_path / "reports/index.html").read_text()
    assert "未実行" in text
    assert "対象commit" in text
    assert "RecipeWeave" in text
    assert "個別テスト結果は未生成" in (tmp_path / "reports/tests.html").read_text()


def test_junit_preserves_parameter_cases_failures_and_skips(tmp_path: Path) -> None:
    (tmp_path / "backend-junit.xml").write_text("""<testsuites><testsuite>
    <testcase classname="API" name="所有権[別ユーザー]" time="0.3">
    <failure>拒否されない</failure></testcase>
    <testcase classname="API" name="作成成功" time="0.1"/>
    <testcase classname="DB" name="実接続"><skipped/></testcase>
    </testsuite></testsuites>""")
    rows = collect_test_results(tmp_path)
    assert [row[3] for row in rows] == ["failed", "passed", "skipped"]
    assert rows[0][2] == "所有権[別ユーザー]"
    assert rows[0][-1] == "拒否されない"


def test_junit_external_entity_definition_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "pytest.xml").write_text('<!DOCTYPE x [<!ENTITY x SYSTEM "file:///secret">]><x/>')
    with pytest.raises(ValueError, match="外部実体"):
        collect_test_results(tmp_path)


def test_docs_slug_and_links_preserve_nested_indexes(tmp_path: Path) -> None:
    source = tmp_path / "docs/design/generated"
    (source / "database").mkdir(parents=True)
    (source / "README.md").write_text("# 全体\n[DB](database/README.md)\n")
    (source / "database/README.md").write_text("# DB一覧\n[戻る](../README.md)\n")
    assert prepare(tmp_path, "/RecipeWeave/quality/design") == 2
    index = tmp_path / "documentation/src/content/docs/index.md"
    assert "/RecipeWeave/quality/design/database/" in index.read_text()
    assert slug("api/README.md") == "api"


def test_docs_link_error_does_not_delete_previous_site_sources(tmp_path: Path) -> None:
    source = tmp_path / "docs/design/generated"
    source.mkdir(parents=True)
    (source / "README.md").write_text("# 全体\n[不明](missing.md)\n")
    existing = tmp_path / "documentation/src/content/docs/index.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("以前の検証済み入力")
    with pytest.raises(ValueError, match="生成対象"):
        prepare(tmp_path)
    assert existing.read_text() == "以前の検証済み入力"


def test_built_html_links_must_resolve_under_reports(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    (reports / "design").mkdir(parents=True)
    (reports / "index.html").write_text("品質")
    page = reports / "design/index.html"
    page.write_text('<a href="/RecipeWeave/quality/">品質</a>')
    assert verify_html(tmp_path, "/RecipeWeave/quality/design") == (1, 1)
    page.write_text('<a href="missing/">不明</a>')
    with pytest.raises(ValueError, match="リンクが切れ"):
        verify_html(tmp_path, "/RecipeWeave/quality/design")


def test_truncated_png_cannot_be_success_evidence(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    path = tmp_path / "truncated.png"
    path.write_bytes(b"\x89PNG\r\n\x1a\n")
    cases, count = collect_cases(playwright_result(str(path)), tmp_path, reports)
    assert count == 0
    assert cases[0]["status"] == "missing"
    assert any("終端" in text for text in cases[0]["errors"])
