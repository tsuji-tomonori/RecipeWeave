"""合成データを使うCIのブラウザ失敗を、認証情報を除いてログにも残す。"""

import os
import re
import uuid
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SENSITIVE_LINE = re.compile(
    r"authorization|bearer|password|passwd|secret|access[_-]?token|refresh[_-]?token|"
    r"id[_-]?token|cookie|パスワード",
    re.IGNORECASE,
)
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")
DATABASE = re.compile(r"postgres(?:ql)?://[^\s\"'<>]+", re.IGNORECASE)
QUERY_SECRET = re.compile(
    r"([?&](?:code|state|token|session|client_secret)=)[^&#\s\"'<>]+", re.IGNORECASE
)


def sanitize(text: str) -> str:
    """認証項目の行は値ごと落とし、URLの資格情報とJWTも取り除く。"""
    lines = []
    for line in text.splitlines():
        if SENSITIVE_LINE.search(line):
            lines.append("[認証情報を含む可能性がある行を非表示]")
            continue
        line = DATABASE.sub("[DB接続URLを非表示]", line)
        line = JWT.sub("[認証トークンを非表示]", line)
        line = QUERY_SECRET.sub(r"\1[非表示]", line)
        lines.append(line)
    return "\n".join(lines)


def read_safe(path: Path, allowed: Path, limit: int) -> str:
    """既知の証跡ディレクトリ内の通常ファイルだけを上限付きで読む。"""
    if (
        path.is_symlink()
        or allowed.is_symlink()
        or any(parent.is_symlink() for parent in path.parents if parent != allowed)
        or not path.resolve().is_relative_to(allowed.resolve())
    ):
        raise ValueError("診断対象のパスが許可された証跡外です")
    data = path.read_bytes()
    if len(data) > limit:
        # 途中で切れた先頭行から、認証項目名だけが落ちることを避ける。
        data = data[-limit:].partition(b"\n")[2]
        prefix = "[末尾のみ。全体はartifact参照]\n"
    else:
        prefix = ""
    return prefix + sanitize(data.decode("utf-8", errors="replace"))


def main() -> None:
    database = urlsplit(os.environ.get("DATABASE_URL", ""))
    if (
        os.environ.get("CI") != "true"
        or os.environ.get("ENVIRONMENT") != "test"
        or os.environ.get("AUTH_MODE") != "local"
        or database.hostname not in {"127.0.0.1", "localhost"}
        or database.path not in {"/recipeweave", "/recipeweave_e2e", "/recipeweave_browser"}
    ):
        raise SystemExit("合成データ専用のローカルCI以外では診断本文を表示しません")
    reports, results = ROOT / "reports", ROOT / "frontend/test-results"
    candidates = [(reports / "api.log", reports, 40000)]
    candidates.extend((path, results, 16000) for path in sorted(results.rglob("error-context.md")))
    marker = uuid.uuid4().hex
    # 診断本文に含まれる文字列をGitHubのworkflow commandとして解釈させない。
    print(f"::stop-commands::{marker}", flush=True)
    try:
        for path, allowed, limit in candidates[:41]:
            if not path.is_file():
                continue
            print(f"\n診断: {path.relative_to(ROOT)}", flush=True)
            print(read_safe(path, allowed, limit), flush=True)
    finally:
        print(f"::{marker}::", flush=True)


if __name__ == "__main__":
    main()
