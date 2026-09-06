"""追跡済み・未追跡の生成差分を検出し、公開用生成物だけを検証記録へ出す。"""

import base64
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    "backend/openapi.gen.json",
    "backend/src/app/apis/state/get_state/generated/queries.py",
    "backend/src/app/apis/state/put_state/generated/queries.py",
    "docs/design/generated",
]


def main() -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", *PATHS],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    if not result.stdout:
        print("生成設計書はコミット済みソースと一致しています。")
        return
    print(result.stdout)
    # 公開するOpenAPI・wrapper・設計書だけを対象とし、リンク先の任意ファイルは読まない。
    paths = [ROOT / path for path in PATHS[:3]]
    paths += sorted((ROOT / "docs/design/generated").rglob("*.md"))
    for path in paths:
        if any(parent.is_symlink() for parent in [path, *path.parents]):
            raise SystemExit("生成物のシンボリックリンクは許可しません")
    data = {str(path.relative_to(ROOT)): path.read_text() for path in paths if path.is_file()}
    raw = json.dumps(data, ensure_ascii=False).encode()
    encoded = base64.b64encode(raw).decode()
    print("GENERATED_SERVICE_SHA256=" + hashlib.sha256(raw).hexdigest())
    for index, start in enumerate(range(0, len(encoded), 32000)):
        print(f"GENERATED_SERVICE_PART_{index:04d}=" + encoded[start : start + 32000])
    raise SystemExit("生成設計書に差分があります。再生成結果をレビューしてコミットしてください")


if __name__ == "__main__":
    main()
