"""固定した依存でLinux Python 3.12用Lambda資材を構築する。Dockerやクラウド接続は不要。"""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--architecture", choices=["x86_64", "arm64"], default="x86_64")
    args = parser.parse_args()
    target = ROOT / "backend/.build/lambda"
    target.parent.mkdir(parents=True, exist_ok=True)
    requirements = target.parent / "runtime-requirements.txt"
    subprocess.run(
        [
            "uv",
            "export",
            "--locked",
            "--package",
            "recipeweave-api",
            "--no-dev",
            "--no-emit-project",
            "--no-emit-workspace",
            "--format",
            "requirements-txt",
            "--output-file",
            str(requirements),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()
    architecture = "aarch64" if args.architecture == "arm64" else "x86_64"
    subprocess.run(
        [
            "uv",
            "pip",
            "install",
            "--require-hashes",
            "--python-version",
            "3.12",
            "--python-platform",
            f"{architecture}-manylinux_2_28",
            "--only-binary",
            ":all:",
            "--target",
            str(target),
            "--requirements",
            str(requirements),
        ],
        cwd=ROOT,
        check=True,
    )
    shutil.copytree(
        ROOT / "backend/src/app",
        target / "app",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "tools"),
    )
    shutil.copytree(ROOT / "data/samples", target / "app/sample_data")
    entries = {
        str(path.relative_to(target)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(target.rglob("*"))
        if path.is_file()
    }
    (target.parent / "lambda-manifest.gen.json").write_text(
        json.dumps(
            {
                "architecture": args.architecture,
                "python": "3.12",
                "files": entries,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"Lambda asset: {target}; {len(entries)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
