"""生成設計を検索可能なサイトへ変換し、公開先の内部リンクを検査する。"""

import argparse
import json
import os
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def slug(name: str) -> str:
    """拡張子と一覧ページの名前を、衝突しないサイト内パスへ正規化する。"""
    parts = name.removesuffix(".md").lower().replace(".", "").split("/")
    if parts[-1] in {"readme", "index"}:
        parts.pop()
    return "/".join(parts)


def safe(path: Path) -> None:
    if any(parent.is_symlink() for parent in [path, *path.parents]):
        raise ValueError(f"シンボリックリンクは使用できません: {path}")


def sources(root: Path) -> dict[Path, str]:
    generated = root / "docs/design/generated"
    result = {
        path: slug(path.relative_to(generated).as_posix()) for path in generated.rglob("*.md")
    }
    for path in (root / "docs/design").glob("*.md"):
        result[path] = slug(path.name)
    requirements = root / "docs/requirements/REQUIREMENTS.md"
    if requirements.exists():
        result[requirements] = "requirements"
    return result


def prepare(root: Path = ROOT, base: str | None = None) -> int:
    base = (base or os.getenv("DOCS_BASE", "/design")).rstrip("/")
    content = root / "documentation/src/content/docs"
    safe(content)
    files = sources(root)
    if not files:
        raise ValueError("生成設計書がありません")
    outputs: dict[str, str] = {}
    json_files = {
        path.resolve(): path.parent.name + ".json"
        for path in (root / "docs/design/generated/api/operations").glob("*/interface.openapi.json")
    }
    for path, name in sorted(files.items()):
        safe(path)
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^\s*<!--.*?-->\s*", "", text, flags=re.DOTALL)
        heading, _, body = text.partition("\n")
        if not heading.startswith("# "):
            raise ValueError(f"設計書に見出しがありません: {path}")

        def replace(match: re.Match[str]) -> str:
            target = unquote(match[1])
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                return match[0]
            if parsed.path.endswith(".json"):
                resolved_json = (path.parent / parsed.path).resolve()
                if resolved_json not in json_files:
                    raise ValueError(f"公開OpenAPIがありません: {target}")
                return "](" + base + "/openapi/" + json_files[resolved_json] + ")"
            if not parsed.path.endswith(".md"):
                return match[0]
            resolved = (path.parent / parsed.path).resolve()
            mapped = {item.resolve(): value for item, value in files.items()}
            if resolved not in mapped:
                raise ValueError(f"文書リンクの生成対象がありません: {path}: {target}")
            destination = base + "/" + (mapped[resolved] + "/" if mapped[resolved] else "")
            return "](" + destination + ("#" + parsed.fragment if parsed.fragment else "") + ")"

        body = re.sub(r"\]\(([^)]+)\)", replace, body)
        destination = name + ".md" if name else "index.md"
        if destination in outputs:
            raise ValueError(f"サイト内パスが衝突しています: {destination}")
        outputs[destination] = (
            "---\ntitle: " + json.dumps(heading[2:].strip(), ensure_ascii=False) + "\n---\n" + body
        )
    # 変換とリンク検査がすべて成功してから、専用ディレクトリだけを置換する。
    if content.exists():
        for path in content.rglob("*"):
            safe(path)
        shutil.rmtree(content)
    for name, text in outputs.items():
        destination = content / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    public = root / "documentation/public/openapi"
    safe(public)
    for old in public.glob("*.json"):
        safe(old)
        old.unlink()
    public.mkdir(parents=True, exist_ok=True)
    for source, name in sorted(json_files.items()):
        safe(source)
        shutil.copyfile(source, public / name)
    return len(outputs)


class Links(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.links: list[str] = []
        self.feed(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link", "script", "img"}:
            self.links.extend(value for key in ("href", "src") if (value := values.get(key)))


def verify_html(root: Path = ROOT, base: str | None = None) -> tuple[int, int]:
    base = (base or os.getenv("DOCS_BASE", "/design")).rstrip("/")
    prefix = base.removesuffix("/design")
    reports = root / "reports"
    pages = sorted((reports / "design").rglob("*.html"))
    count = 0
    if not pages:
        raise ValueError("ビルド済み設計サイトがありません")
    for page in pages:
        for target in Links(page.read_text()).links:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = unquote(parsed.path)
            if prefix and path.startswith(prefix + "/"):
                path = path[len(prefix) :]
            destination = (
                reports / path.lstrip("/") if path.startswith("/") else page.parent / path
            ).resolve()
            if destination.is_dir():
                destination /= "index.html"
            if not destination.is_relative_to(reports.resolve()) or not destination.is_file():
                raise ValueError(f"公開HTMLのリンクが切れています: {page}: {target}")
            count += 1
    return len(pages), count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if not args.verify_only:
        print(f"設計サイト入力: {prepare()} ページ")
    if args.prepare_only:
        return
    if not args.verify_only:
        subprocess.run(
            ["npm", "--prefix", "documentation", "run", "build", "--", "--force"],
            cwd=ROOT,
            check=True,
        )
    pages, links = verify_html()
    print(f"公開HTML: {pages} ページ / 内部リンク・資源: {links} 件")


if __name__ == "__main__":
    main()
