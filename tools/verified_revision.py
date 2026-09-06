"""成功したdevのコミットとツリーだけをmain配備の根拠として受け付ける。"""

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def matches(proof, *, source, commit, tree):
    lines = proof.splitlines()
    return (
        len(lines) == 3
        and all(re.fullmatch(r"[0-9a-f]{40}", value) for value in lines)
        and lines == [source, commit, tree]
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    if args.write:
        source = os.environ["SOURCE_SHA"]
        commit, tree = git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")
        proof = f"{source}\n{commit}\n{tree}\n"
        if not matches(proof, source=source, commit=commit, tree=tree):
            raise SystemExit("検証証跡のSHAが不正です")
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(proof)
        return
    subprocess.run(["git", "fetch", "origin", "dev"], check=True)
    tree, dev_tree = git("rev-parse", "HEAD^{tree}"), git("rev-parse", "origin/dev^{tree}")
    if tree != dev_tree:
        raise SystemExit("mainとdevのツリーが一致しません")
    dev = git("rev-parse", "origin/dev")
    runs = json.loads(
        subprocess.check_output(
            [
                "gh",
                "run",
                "list",
                "--workflow",
                "dev.yml",
                "--branch",
                "dev",
                "--event",
                "push",
                "--status",
                "success",
                "--limit",
                "30",
                "--json",
                "databaseId,headSha",
            ],
            text=True,
        )
    )
    for run in runs:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    "gh",
                    "run",
                    "download",
                    str(run["databaseId"]),
                    "--name",
                    "verified-revision",
                    "--dir",
                    directory,
                ],
                capture_output=True,
                check=False,
            )
            proof = Path(directory) / "verified-revision.txt"
            if (
                result.returncode == 0
                and proof.is_file()
                and matches(proof.read_text(), source=run["headSha"], commit=dev, tree=tree)
            ):
                print(f"成功run {run['databaseId']} のdevコミット・ツリーとの一致を確認しました")
                return
    raise SystemExit(
        "このコミット・ツリーを証明する成功済みdev pushがありません。devを再検証してください"
    )


if __name__ == "__main__":
    main()
