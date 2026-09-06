"""JUnitとVitestの実行結果を、展開済みテストケースとして一覧化する。"""

import ast
import html
import json
from xml.etree import ElementTree as ET


def test_results(reports):
    rows = []
    descriptions = {}
    root = reports.parent
    for path in (root / "backend/tests").glob("test_*.py"):
        parsed = ast.parse(path.read_text())
        for node in ast.walk(parsed):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith(
                "test_"
            ):
                description = ast.get_docstring(node)
                if description:
                    descriptions[
                        (str(path.relative_to(root).with_suffix("")).replace("/", "."), node.name)
                    ] = description

    for junit in sorted(set(reports.glob("*-junit.xml")) | set(reports.glob("pytest.xml"))):
        raw = junit.read_text()
        if "<!DOCTYPE" in raw or "<!ENTITY" in raw:
            raise ValueError("JUnitの外部実体定義は使用できません")
        for case in ET.fromstring(raw).iter("testcase"):
            failure = case.find("failure")
            error = case.find("error")
            state = (
                "skipped"
                if case.find("skipped") is not None
                else "failed"
                if failure is not None or error is not None
                else "passed"
            )
            raw_name = case.get("name", "")
            description = descriptions.get((case.get("classname", ""), raw_name.split("[")[0]))
            display_name = (description + "（" + raw_name + "）") if description else raw_name
            rows.append(
                (
                    junit.stem.removesuffix("-junit"),
                    case.get("classname", ""),
                    display_name,
                    state,
                    case.get("time", "0"),
                    (
                        failure.text
                        if failure is not None
                        else error.text
                        if error is not None
                        else ""
                    )
                    or "",
                )
            )
    vitest = reports / "vitest.json"
    if vitest.exists():
        for suite in json.loads(vitest.read_text()).get("testResults", []):
            name = suite["name"].split("/frontend/")[-1]
            for case in suite.get("assertionResults", []):
                rows.append(
                    (
                        "Vitest",
                        name,
                        case["fullName"],
                        case["status"],
                        str(case.get("duration", 0) / 1000),
                        "\n".join(case.get("failureMessages", [])),
                    )
                )
    return rows


def render_results(reports):
    rows = test_results(reports)
    if not rows:
        return '<p class="notice">個別テスト結果は未生成です。</p>'
    groups = {}
    for runner, file, title, state, duration, error in rows:
        groups.setdefault((runner, file), []).append((title, state, duration, error))
    labels = {"passed": "成功", "failed": "失敗", "skipped": "スキップ", "pending": "未実行"}
    result = (
        f"<h2>個別テスト一覧</h2><p>実行結果 {len(rows)}件。"
        "pytestのパラメーター展開後とVitestの各ケースを表示します。</p>"
    )
    for (runner, file), cases in groups.items():
        result += (
            f'<section class="panel unit-suite"><h3>'
            f"{html.escape(runner + ' / ' + file)}</h3>"
            f'<div class="table-wrap"><table><thead>'
            f"<tr><th>テストケース</th><th>結果</th><th>秒</th>"
            f"</tr></thead><tbody>"
        )
        for title, state, duration, error in cases:
            result += (
                f"<tr><td>{html.escape(title)}</td><td>"
                f"{labels.get(state, html.escape(state))}</td>"
                f"<td>{float(duration):.3f}</td></tr>"
            )
            if error:
                result += '<tr><td colspan="3"><pre>' + html.escape(error) + "</pre></td></tr>"
        result += "</tbody></table></div></section>"
    return result
