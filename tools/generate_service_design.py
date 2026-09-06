"""Generate a service inventory from code, OpenAPI, samples and synthesized CDK."""

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/design/generated/service.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render() -> str:
    openapi_path = ROOT / "backend/openapi.gen.json"
    spec = json.loads(openapi_path.read_text())
    foods = json.loads((ROOT / "data/samples/foods.json").read_text())
    recipes = json.loads((ROOT / "data/samples/recipes.json").read_text())
    lines = [
        "# サービス実装由来の設計",
        "",
        "生成元: OpenAPI・TypeScript/Python実装・SQL・サンプルJSON・CDK合成結果。手編集禁止。",
        "`uv run python tools/generate_service_design.py` で生成、`--check` で差分検査。",
        "コードと配備定義の存在を示す。実配備・実機評価・OCR精度の実測を証明するものではない。",
        "",
        "## サンプルデータ",
        "",
        f"食材 {len(foods)} 件、料理 {len(recipes)} 件。"
        "完成レシピの本番カタログとは別のDev用標本。",
        "",
        "| ファイル | SHA-256 |",
        "|---|---|",
    ]
    for path in sorted((ROOT / "data/samples").glob("*.json")):
        lines.append(f"| `{path.relative_to(ROOT)}` | `{digest(path)}` |")
    lines += [
        "", "## API", "",
        "| Method | Path | operationId | 認証定義 | 応答 |",
        "|---|---|---|---|---|",
    ]
    for route, value in sorted(spec["paths"].items()):
        for method, op in sorted(value.items()):
            if method not in {"get", "post", "put", "patch", "delete", "head", "options"}:
                continue
            security = op.get("security", spec.get("security", []))
            names = sorted({name for requirement in security for name in requirement})
            lines.append(
                f"| {method.upper()} | `{route}` | `{op.get('operationId', '')}` | "
                f"{', '.join(names) or '公開'} | {', '.join(sorted(op['responses']))} |"
            )
    lines += ["", "## 実装の公開要素", "", "| ファイル | 公開要素 | SHA-256 |", "|---|---|---|"]
    paths = sorted((ROOT / "frontend/src").rglob("*.ts"))
    paths += sorted((ROOT / "frontend/src").rglob("*.svelte"))
    for path in paths:
        text = path.read_text()
        exports = re.findall(
            r"export\s+(?:async\s+)?(?:function|class|interface|type|const)\s+(\w+)", text
        )
        fallback = (
            "検証コード" if path.name.endswith(".test.ts") else "画面コンポーネント／起動処理"
        )
        public = ", ".join(f"`{name}`" for name in exports) or fallback
        lines.append(f"| `{path.relative_to(ROOT)}` | {public} | `{digest(path)}` |")
    lines += ["", "## SQL境界", "", "| SQL | SHA-256 |", "|---|---|"]
    sql_paths = sorted((ROOT / "backend/src").rglob("*.sql"))
    sql_paths += sorted((ROOT / "database").rglob("*.sql"))
    for path in sql_paths:
        lines.append(f"| `{path.relative_to(ROOT)}` | `{digest(path)}` |")
    lines += [
        "", "## CDK合成資源", "",
        "以下は合成テンプレートの資源定義。アカウントへの作成結果ではない。",
    ]
    for stack in ("Data", "Service"):
        path = ROOT / f"infra/cdk.out/RecipeWeave-dev-{stack}.template.json"
        template = json.loads(path.read_text())
        resources = template["Resources"]
        counts = Counter(resource["Type"] for resource in resources.values())
        lines += ["", f"### {stack}", "", "| 資源種別 | 数 |", "|---|---|"]
        lines += [f"| `{kind}` | {count} |" for kind, count in sorted(counts.items())]
        lines += ["", "| Logical ID | 資源種別 |", "|---|---|"]
        lines += [
            f"| `{name}` | `{resource['Type']}` |"
            for name, resource in sorted(resources.items())
        ]
    lines += [
        "", "## 再現と受入の境界", "",
        "- 画面の型検査・状態計算テストと、APIの型検査・認証/競合テストを別々に実行する。",
        "- OpenAPIとSQL wrapperは `app-docs --check`、本書は `--check` で追従を確認する。",
        "- CDK構造検査と合成は配備前の検証。DSQL実接続・Cognito実ログインは別の受入を要する。",
        "- 設計判断は [ADR-0001](../ADR-0001-service-dev.md) を参照する。", "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUT.is_file() or OUT.read_text() != expected:
            raise SystemExit("generated service design drift")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(expected)


if __name__ == "__main__":
    main()
