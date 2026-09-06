"""Fail on tracked or untracked design drift and expose only public generated files."""

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
    "docs/design/generated/generator.md",
    "docs/design/generated/service.md",
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
        print("Generated service design matches the committed source.")
        return
    print(result.stdout)
    # These exact files contain public code/schema only. No arbitrary files or environment values.
    data = {path: (ROOT / path).read_text() for path in PATHS if (ROOT / path).is_file()}
    raw = json.dumps(data, ensure_ascii=False).encode()
    encoded = base64.b64encode(raw).decode()
    print("GENERATED_SERVICE_SHA256=" + hashlib.sha256(raw).hexdigest())
    for index, start in enumerate(range(0, len(encoded), 32000)):
        print(f"GENERATED_SERVICE_PART_{index:04d}=" + encoded[start : start + 32000])
    raise SystemExit("generated service design drift; review and commit regenerated files")


if __name__ == "__main__":
    main()
