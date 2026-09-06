"""生成書式、入力ハッシュ、管理対象ファイルの検査を共通化する。"""

import hashlib
import html
from pathlib import Path


class DesignError(ValueError):
    """未対応構造や入力の不整合を、出力を書き換える前に知らせる。"""


def read_source(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise DesignError(f"シンボリックリンクは入力にできません: {relative}")
    return path.read_text(encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cell(value: object) -> str:
    return html.escape(str(value), quote=False).replace("|", "&#124;").replace("\n", " ")


def table(headers: list[str], rows: list[list[object]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "|" + "|".join("---" for _ in headers) + "|",
            *("| " + " | ".join(cell(item) for item in row) + " |" for row in rows),
        ]
    )


def document(title: str, sections: list[str]) -> str:
    return (
        "\n\n".join(
            [
                f"# {title}",
                "実装から自動生成。手編集禁止。"
                "`uv run python tools/generate_service_design.py` で更新。",
                *sections,
            ]
        ).rstrip()
        + "\n"
    )
