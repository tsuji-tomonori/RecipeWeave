"""固定した依存でLinux Python 3.12用Lambda資材を構築する。Dockerやクラウド接続は不要。"""

import argparse
import base64
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def file_hashes(target: Path) -> dict[str, str]:
    """一時bytecodeを拒否し、配備対象の全バイトを検査する。"""
    entries: dict[str, str] = {}
    for path in sorted(target.rglob("*")):
        if path.name == "__pycache__" or path.suffix in {".pyc", ".pyo"}:
            raise ValueError(
                f"Lambda資材に一時bytecodeが混入しています: {path.relative_to(target)}"
            )
        if path.is_file():
            entries[str(path.relative_to(target))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return entries


def normalize_entrypoints(target: Path) -> None:
    """uvが埋め込む構築機固有のPythonパスを可搬な起動方法へそろえる。"""
    changed: set[str] = set()
    for script in sorted((target / "bin").glob("*")):
        if not script.is_file():
            continue
        first, separator, rest = script.read_bytes().partition(b"\n")
        if first.startswith(b"#!") and b"python" in first:
            script.write_bytes(b"#!/usr/bin/env python3.12" + separator + rest)
            changed.add(str(script.relative_to(target)))
    recorded: set[str] = set()
    for record in sorted(target.glob("*.dist-info/RECORD")):
        with record.open(newline="") as stream:
            rows = list(csv.reader(stream))
        modified = False
        for row in rows:
            if len(row) != 3:
                raise ValueError(f"wheel RECORDの形式が不正です: {record.name}")
            name = row[0]
            if name in changed:
                content = (target / name).read_bytes()
                digest = (
                    base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
                )
                row[1:] = [f"sha256={digest}", str(len(content))]
                recorded.add(name)
                modified = True
        if modified:
            with record.open("w", newline="") as stream:
                csv.writer(stream, lineterminator="\n").writerows(rows)
    if changed != recorded:
        raise ValueError(
            f"起動スクリプトに対応するRECORDがありません: {sorted(changed - recorded)}"
        )


def export_requirements(requirements: Path) -> None:
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


def build_asset(target: Path, requirements: Path, requested_architecture: str) -> dict[str, str]:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()
    architecture = "aarch64" if requested_architecture == "arm64" else "x86_64"
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
        # 開発者のuv設定でbytecodeを生成しても、配備資材へ持ち込まない。
        env={**os.environ, "UV_COMPILE_BYTECODE": "false"},
    )
    normalize_entrypoints(target)
    shutil.copytree(
        ROOT / "backend/src/app",
        target / "app",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "tools"),
    )
    # 移行専用LambdaにSQLとchecksum台帳を同梱する。
    shutil.copytree(
        ROOT / "database",
        target / "database",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    # 同じCPUの環境では、開発用site-packagesに依存せず両handlerをimportできることを確認する。
    before_import = file_hashes(target)
    if platform.system() == "Linux" and platform.machine() in {
        architecture,
        requested_architecture,
    }:
        subprocess.run(
            [
                sys.executable,
                "-B",
                "-I",
                "-S",
                "-c",
                "import sys; sys.path.insert(0, sys.argv[1]); "
                "import app.handler; import app.integrations.database.migration_handler",
                str(target),
            ],
            cwd=ROOT,
            check=True,
        )
    entries = file_hashes(target)
    if entries != before_import:
        raise ValueError("handlerのimport検証が配備資材を書き換えました")
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--architecture", choices=["x86_64", "arm64"], default="x86_64")
    parser.add_argument(
        "--verify-reproducible", action="store_true", help="別の出力先でも構築し全バイトを照合する"
    )
    args = parser.parse_args()
    target = ROOT / "backend/.build/lambda"
    target.parent.mkdir(parents=True, exist_ok=True)
    requirements = target.parent / "runtime-requirements.txt"
    export_requirements(requirements)
    entries = build_asset(target, requirements, args.architecture)
    if args.verify_reproducible:
        with tempfile.TemporaryDirectory(prefix="recipeweave-lambda-repro-") as directory:
            repeated = build_asset(Path(directory) / "lambda", requirements, args.architecture)
        if entries != repeated:
            changed = sorted(
                name
                for name in entries.keys() | repeated.keys()
                if entries.get(name) != repeated.get(name)
            )
            raise ValueError(f"同じ入力からのLambda再構築が一致しません: {changed}")
        print(f"Lambda再現性: 異なる出力先の全{len(entries)}ファイルが一致しました")
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
