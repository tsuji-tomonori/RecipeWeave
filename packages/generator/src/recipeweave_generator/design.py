"""実装済みのPython構成から設計を生成し、将来のアプリを実装済みとは記載しない。"""

import argparse
import ast
import hashlib
from pathlib import Path


def render(root: Path) -> str:
    lines = [
        "# 実装由来の設計",
        "",
        "生成元: Python AST。手編集禁止。",
        "",
        "`uv run python -m recipeweave_generator.design` で再生成し、`--check` で差分検査。",
        "",
        "| 実装ファイル | SHA-256 | 公開定義 |",
        "|---|---|---|",
    ]
    for path in sorted((root / "packages/generator/src/recipeweave_generator").glob("*.py")):
        data = path.read_bytes()
        tree = ast.parse(data)
        public = [
            n.name
            for n in tree.body
            if isinstance(n, ast.FunctionDef | ast.ClassDef) and not n.name.startswith("_")
        ]
        lines.append(
            f"| `{path.relative_to(root)}` | `{hashlib.sha256(data).hexdigest()}` | "
            + ", ".join(f"`{n}`" for n in public)
            + " |"
        )
    lines += ["", "## 境界", "", "| ディレクトリ | 現在の役割 |", "|---|---|"]
    boundaries = {
        "frontend": ("src/main.ts", "Svelte画面・端末保存・レシートOCR・数量計算"),
        "backend": ("src/app/main.py", "FastAPI・カタログAPI・認証付き状態API"),
        "database": ("README.md", "DSQLマイグレーションと運用手順"),
        "infra": ("bin/recipeweave.ts", "AWS CDKによる配備定義"),
    }
    for name in ("frontend", "backend", "database", "infra", "batch", "scripts"):
        if (root / name / "moon.yml").is_file():
            boundary = boundaries.get(name)
            role = (
                boundary[1]
                if boundary and (root / name / boundary[0]).is_file()
                else "moonプロジェクトの場所を確保。製品機能は未実装"
            )
            lines.append(f"| `{name}` | {role} |")
    lines += [
        "",
        "コードの存在に基づく列挙。サービス詳細は [service.md](service.md)、",
        "実際の検証・公開状況はサービス受入記録で確認する。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    root = Path.cwd()
    out = root / "docs/design/generated/generator.md"
    if any(parent.is_symlink() for parent in [out, *out.parents] if parent != root.parent):
        raise ValueError("refuse symlink output")
    text = render(root)
    if args.check:
        if not out.is_file() or out.read_text() != text:
            raise SystemExit("generated design drift")
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)


if __name__ == "__main__":
    main()
