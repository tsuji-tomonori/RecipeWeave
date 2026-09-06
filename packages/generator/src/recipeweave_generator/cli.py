"""明示したオフラインコマンドだけを実行し、モデルAPIや有料生成は呼び出さない。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .catalog import compile_files
from .export import atomic_json, export_all, verify_all
from .space import Space


def main() -> None:
    parser = argparse.ArgumentParser(prog="recipeweave")
    sub = parser.add_subparsers(dest="command", required=True)
    compile_cmd = sub.add_parser("compile")
    compile_cmd.add_argument("--catalog", type=Path, default=Path("data/catalog"))
    for name in ("count", "show", "sample", "export"):
        p = sub.add_parser(name)
        p.add_argument("--definition", type=Path, default=Path("data/catalog/v3_reviewed.json"))
        if name == "show":
            p.add_argument("--ordinal", type=int, required=True)
        if name == "sample":
            p.add_argument("--size", type=int, required=True)
            p.add_argument("--seed", type=int, required=True)
            p.add_argument("--output", type=Path, required=True)
        if name == "export":
            p.add_argument("--output", type=Path, required=True)
            p.add_argument("--shard-size", type=int, default=1_000_000)
    verify = sub.add_parser("verify-export")
    verify.add_argument("--output", type=Path, required=True)
    verify.add_argument("--definition", type=Path)
    verify.add_argument("--full", action="store_true", help="compare every row with its definition")
    args = parser.parse_args()
    if args.command == "compile":
        result = compile_files(args.catalog)
    elif args.command == "verify-export":
        result = verify_all(
            args.output, Space.load(args.definition) if args.definition else None, full=args.full
        )
    else:
        space = Space.load(args.definition)
        if args.command == "count":
            result = {"total": space.total, "sha256": space.digest}
        elif args.command == "show":
            result = {
                "ordinal": args.ordinal,
                "signature": space.signature(args.ordinal),
                **space.describe(args.ordinal),
            }
        elif args.command == "sample":
            sample = [
                {"id": f"S{i:05d}", "ordinal": n, **space.describe(n)}
                for i, n in enumerate(space.sample(args.size, args.seed))
            ]
            atomic_json(args.output, sample)
            result = {"n": len(sample), "seed": args.seed, "definition_sha256": space.digest}
        else:
            result = export_all(space, args.output, args.shard_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
