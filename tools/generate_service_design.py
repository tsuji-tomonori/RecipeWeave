"""実装・DDL・SQL・OpenAPI・CDKから設計書一式を決定的に生成する。"""

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/design/generated"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(root: Path = ROOT) -> str:
    openapi_path = root / "backend/openapi.gen.json"
    spec = json.loads(openapi_path.read_text())
    foods = json.loads((root / "data/samples/foods.json").read_text())
    recipes = json.loads((root / "data/samples/recipes.json").read_text())
    lines = [
        "# サービス実装由来の設計",
        "",
        "生成元: OpenAPI・TypeScript/Python実装・SQL・サンプルJSON・CDK合成結果。手編集禁止。",
        "`uv run python tools/generate_service_design.py` で生成、`--check` で差分検査。",
        "コードと配備定義の存在を示す。実配備・実機評価・OCR精度の実測を証明するものではない。",
        "",
        "## 再現用の旧サンプル入力",
        "",
        f"食材 {len(foods)} 件、料理 {len(recipes)} 件。"
        "初期検証に用いた標本。公開APIの実データ取得元は各SQL仕様、正規化DBへの投入はdatabase/seed.pyを参照する。",
        "",
        "| ファイル | SHA-256 |",
        "|---|---|",
    ]
    for path in sorted((root / "data/samples").glob("*.json")):
        lines.append(f"| `{path.relative_to(root)}` | `{digest(path)}` |")
    lines += [
        "",
        "## API",
        "",
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
    paths = sorted((root / "frontend/src").rglob("*.ts"))
    paths += sorted((root / "frontend/src").rglob("*.svelte"))
    for path in paths:
        text = path.read_text()
        exports = re.findall(
            r"export\s+(?:async\s+)?(?:function|class|interface|type|const)\s+(\w+)", text
        )
        fallback = (
            "検証コード" if path.name.endswith(".test.ts") else "画面コンポーネント／起動処理"
        )
        public = ", ".join(f"`{name}`" for name in exports) or fallback
        lines.append(f"| `{path.relative_to(root)}` | {public} | `{digest(path)}` |")
    lines += ["", "## SQL境界", "", "| SQL | SHA-256 |", "|---|---|"]
    sql_paths = sorted((root / "backend/src").rglob("*.sql"))
    sql_paths += sorted((root / "database").rglob("*.sql"))
    for path in sql_paths:
        lines.append(f"| `{path.relative_to(root)}` | `{digest(path)}` |")
    lines += [
        "",
        "## CDK合成資源",
        "",
        "以下は合成テンプレートの資源定義。アカウントへの作成結果ではない。",
    ]
    for stack in ("Data", "Service"):
        path = root / f"infra/cdk.out/RecipeWeave-dev-{stack}.template.json"
        template = json.loads(path.read_text())
        resources = template["Resources"]
        counts = Counter(resource["Type"] for resource in resources.values())
        lines += ["", f"### {stack}", "", "| 資源種別 | 数 |", "|---|---|"]
        lines += [f"| `{kind}` | {count} |" for kind, count in sorted(counts.items())]
        lines += ["", "| Logical ID | 資源種別 |", "|---|---|"]
        lines += [
            f"| `{name}` | `{resource['Type']}` |" for name, resource in sorted(resources.items())
        ]
    lines += [
        "",
        "## 再現と受入の境界",
        "",
        "- 画面の型検査・状態計算テストと、APIの型検査・認証/競合テストを別々に実行する。",
        "- OpenAPIとSQL wrapperは `app-docs --check`、本書は `--check` で追従を確認する。",
        "- CDK構造検査と合成は配備前の検証。"
        "配備先のPostgreSQL実接続・Cognito実ログインは別の受入を要する。",
        "- 現行の設計判断は [ADR-0002](../ADR-0002-relational-service.md)、"
        "初期構成の履歴は [ADR-0001](../ADR-0001-service-dev.md) を参照する。",
        "",
    ]
    return "\n".join(lines)


def build_outputs(root: Path = ROOT) -> dict[str, str]:
    from tools.design.api import load_operations, render_api
    from tools.design.common import document, read_source, table
    from tools.design.database import load_queries, load_tables, render_database

    spec = json.loads(read_source(root / "backend/openapi.gen.json", root))
    operations = load_operations(root, spec)
    tables = load_tables(root)
    queries = load_queries(root, tables, {op.slug: op.id for op in operations})
    outputs = {"service.md": render(root)}
    outputs.update(render_database(tables, queries))
    if (root / "database/schema-policy.json").exists():
        from database.schema_catalog import extract
        from tools.design.postgres import inspect_postgres

        catalog = extract(root)
        contracts = inspect_postgres(root, catalog)["statements"]
        original = json.loads(read_source(root / "spec/database/source-sheet.json", root))
        mapping = []
        for row in original["tabs"]["01_テーブル一覧"][1:]:
            _, domain, name, meaning, expected_columns, *_ = row
            physical = tables["recipeweave." + name]
            mapping.append(
                [
                    name,
                    domain,
                    meaning,
                    expected_columns,
                    len(physical.columns),
                    f"[実DDL仕様](tables/recipeweave.{name}.md)",
                ]
            )
        outputs["database/SOURCE-MAPPING.md"] = document(
            "Driveの原DB設計と物理実装の対応",
            [
                "原表を一つずつ実DDLへ照合する。原設計の全列型・NULL性もカタログ生成時に確認し、追加列と変更根拠はschema-policyのcolumn_evolutionsで明示する。",
                table(["原テーブル", "領域", "意味", "原列数", "実列数", "物理実装"], mapping),
                "移行台帳、レシート等の追加表は [全物理テーブル一覧](README.md) に含める。",
            ],
        )
        outputs["database/CONTRACTS.md"] = document(
            "移行・索引・DB内部契約",
            [
                "全移行をPostgreSQL文法で解析する。関数本体はソースとして示し、DB内実行の受入は結合テスト結果で確認する。",
                table(["定義元", "SQL構文種別"], [[c["source"], c["kind"]] for c in contracts]),
                *(
                    f"## {c['source']}\n\n```sql\n{c['sql']}\n```"
                    for c in contracts
                    if c["kind"] not in {"CreateStmt", "IndexStmt"}
                ),
            ],
        )
    outputs.update(render_api(root, operations, spec, tables, queries))
    outputs["README.md"] = document(
        "実装から自動生成した設計書",
        [
            f"{len(tables)} テーブル・{len(operations)} API・"
            f"{len({q.source for q in queries})} SQLファイルを対象とする。"
            f"共有呼出しを含むAPIとSQLの対応は {len(queries)} 件。",
            "[原設計との対応](database/SOURCE-MAPPING.md) / [テーブル一覧](database/README.md) / "
            "[ER図](database/ER.md) / "
            "[API一覧](api/README.md) / [CRUD](api/CRUD.md)",
            "[APIモデル・enum](api/MODELS.md) / [共通エラー](api/ERRORS.md) / "
            "[サービス・CDK](service.md) / [レシピ生成](generator.md)",
            "[出力一覧](REGISTRY.md) / [生成元・ハッシュ](MANIFEST.md)",
            "APIごとのインターフェース・詳細設計・ログ・SQL・シーケンス・要因別テストの6帳票と、単独のSwagger互換JSONはAPI一覧から参照できる。",
            "生成方法と解析範囲は [開発者向け手順](../AUTOMATION.md) を参照。"
            "実装の存在を示す資料であり、未実施の本番接続や受入を完了扱いしない。",
        ],
    )
    outputs["REGISTRY.md"] = document(
        "自動生成ファイル一覧",
        [
            table(
                ["ファイル", "区分"],
                [
                    [f"[{name}]({name})", name.split("/")[0]]
                    for name in sorted([*outputs, "REGISTRY.md", "MANIFEST.md"])
                ],
            ),
            "generator.mdは独立したレシピ生成器の設計生成コマンドが管理する。",
        ],
    )
    inputs = {
        root / "backend/openapi.gen.json",
        root / "backend/generators.manual.json",
        root / "database/design.manual.json",
        root / "tools/generate_service_design.py",
        root / "pyproject.toml",
        root / "uv.lock",
        root / ".sqlfluff",
    }
    for directory, patterns in {
        "backend/src": ("*.py", "*.sql", "*.json"),
        "backend/tests": ("*.py",),
        "database": ("*.py", "*.sql", "*.json"),
        "tools/design": ("*.py",),
        "data/samples": ("*.json",),
        "database/seed_data": ("*.json",),
        "spec/database": ("*.json",),
        "frontend/src": ("*.ts", "*.svelte"),
        "infra/lib": ("*.ts",),
        "infra/cdk.out": ("*.template.json",),
    }.items():
        for pattern in patterns:
            inputs.update((root / directory).rglob(pattern))
    source_rows = []
    for path in sorted(inputs):
        read_source(path, root)
        source_rows.append([str(path.relative_to(root)), digest(path)])
    outputs["MANIFEST.md"] = document(
        "設計生成の入力・出力ハッシュ",
        [
            "時刻・絶対パス・実行環境の秘密情報は出力しない。SHA-256はUTF-8ファイルのバイト列を対象とする。",
            "## 入力\n\n" + table(["生成元", "SHA-256"], source_rows),
            "## 出力\n\n"
            + table(
                ["生成物", "SHA-256"],
                [
                    [name, hashlib.sha256(text.encode()).hexdigest()]
                    for name, text in sorted(outputs.items())
                ],
            ),
            "自己参照を避けるためMANIFEST.md自身のハッシュは掲載しない。",
        ],
    )
    return outputs


def main() -> None:
    # ファイルとしての起動とモジュール起動で、同じローカルパッケージを使う。
    sys.path.insert(0, str(ROOT))
    from tools.design.common import DesignError
    from tools.design.storage import synchronize

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="書き込まずに欠落・変更・余剰を検査")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        synchronize(OUT, outputs, check=args.check)
    except (DesignError, OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(f"設計書 {len(outputs)} ファイル: " + ("差分なし" if args.check else "生成完了"))


if __name__ == "__main__":
    main()
