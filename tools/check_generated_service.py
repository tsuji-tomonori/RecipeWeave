"""Fail on tracked or untracked design drift and expose only public generated files."""

import base64
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
    encoded = base64.b64encode(json.dumps(data, ensure_ascii=False).encode()).decode()
    print("GENERATED_SERVICE_SNAPSHOT=" + encoded)
    raise SystemExit("generated service design drift; review and commit regenerated files")


if __name__ == "__main__":
    main()
