"""すべての設計点を行として出力し、マニフェストで実データの代わりにしない。"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
from typing import Any

from .space import Space, canonical


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path: Path, value: Any, compact: bool = False) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    if compact:
        temp.write_bytes(canonical(value) + b"\n")
    else:
        temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    os.replace(temp, path)


def export_all(space: Space, output: Path, shard_size: int = 1_000_000) -> dict[str, Any]:
    if shard_size <= 0:
        raise ValueError("shard size must be positive")
    output.mkdir(parents=True, exist_ok=True)
    path = output / "manifest.json"
    foods = sorted(space.names)
    food_idx = {x: i for i, x in enumerate(foods)}
    flavors = sorted({f for b in space.blocks for f in b["flavors"]})
    flavor_idx = {x: i for i, x in enumerate(flavors)}
    routes = sorted({r for b in space.blocks for r in b["routes"]})
    route_idx = {x: i for i, x in enumerate(routes)}
    dictionary = {
        "foods": [{"id": x, "name": space.names[x]} for x in foods],
        "templates": [{"id": b["code"], "name": b["label"]} for b in space.blocks],
        "flavors": flavors,
        "routes": routes,
    }
    manifest = {
        "schema_version": 1,
        "definition_sha256": space.digest,
        "total": space.total,
        "shard_size": shard_size,
        "status": "incomplete",
        "shards": [],
        "dictionary_sha256": hashlib.sha256(canonical(dictionary)).hexdigest(),
        "columns": [
            "ordinal",
            "template",
            "main",
            "support1",
            "support2",
            "support3",
            "flavor",
            "route",
        ],
        "note": "0-based dictionary indexes; blank means absent. Hypotheses, not cooked recipes.",
    }
    if path.exists():
        existing = json.loads(path.read_text())
        for key in ("definition_sha256", "shard_size", "dictionary_sha256", "total"):
            if existing[key] != manifest[key]:
                raise ValueError("cannot resume output from a different definition")
        manifest = existing
    atomic_json(output / "dictionary.json", dictionary)
    atomic_json(path, manifest)
    seen = {entry["start"]: entry for entry in manifest["shards"]}
    for start in range(0, space.total, shard_size):
        stop = min(space.total, start + shard_size)
        name = f"part-{start // shard_size:05d}.csv.gz"
        dest = output / name
        if start in seen:
            entry = seen[start]
            if (
                entry["stop"] != stop
                or entry["rows"] != stop - start
                or file_hash(dest) != entry["sha256"]
            ):
                raise ValueError("completed shard is corrupt; recover before resuming")
            continue
        temp = dest.with_suffix(".tmp")
        count = 0
        with (
            temp.open("wb") as raw,
            gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=6) as gz,
        ):
            with io.TextIOWrapper(gz, encoding="utf-8", newline="") as text:
                writer = csv.writer(text, lineterminator="\n")
                writer.writerow(manifest["columns"])
                for ordinal, (t, main, aux, flavor, route) in space.iter_range(start, stop):
                    writer.writerow(
                        [
                            ordinal,
                            t,
                            food_idx[main],
                            *[food_idx[x] for x in aux],
                            *[""] * (3 - len(aux)),
                            flavor_idx[flavor],
                            route_idx[route],
                        ]
                    )
                    count += 1
        if count != stop - start:
            raise AssertionError("incomplete shard")
        os.replace(temp, dest)
        manifest["shards"].append(
            {
                "file": name,
                "start": start,
                "stop": stop,
                "rows": count,
                "bytes": dest.stat().st_size,
                "sha256": file_hash(dest),
            }
        )
        atomic_json(path, manifest)
    manifest["status"] = "complete"
    atomic_json(path, manifest)
    return manifest


def verify_all(output: Path, space: Space | None = None) -> dict[str, int]:
    m = json.loads((output / "manifest.json").read_text())
    d = json.loads((output / "dictionary.json").read_text())
    if (
        m["status"] != "complete"
        or hashlib.sha256(canonical(d)).hexdigest() != m["dictionary_sha256"]
    ):
        raise ValueError("incomplete export or dictionary corruption")
    if space is not None and (space.digest != m["definition_sha256"] or space.total != m["total"]):
        raise ValueError("definition mismatch")
    check_ordinals = set(space.sample(min(1024, space.total), 92473)) if space else set()
    if space:
        check_ordinals.update(n for e in m["shards"] for n in (e["start"], e["stop"] - 1))
    checked_points = 0
    expected = 0
    for entry in m["shards"]:
        path = output / entry["file"]
        if entry["start"] != expected or file_hash(path) != entry["sha256"]:
            raise ValueError("noncontiguous or corrupt shard")
        count = 0
        with gzip.open(path, "rt", newline="") as f:
            reader = csv.reader(f)
            if next(reader) != m["columns"]:
                raise ValueError("invalid columns")
            for row in reader:
                if len(row) != 8 or int(row[0]) != expected:
                    raise ValueError("missing, duplicate, or out-of-order row")
                if not 0 <= int(row[1]) < len(d["templates"]):
                    raise ValueError("invalid template")
                ingredient_ids = [int(x) for x in row[2:6] if x]
                if len(set(ingredient_ids)) != len(ingredient_ids):
                    raise ValueError("repeated ingredient")
                if any(not 0 <= x < len(d["foods"]) for x in ingredient_ids):
                    raise ValueError("unknown food")
                if not 0 <= int(row[6]) < len(d["flavors"]) or not 0 <= int(row[7]) < len(
                    d["routes"]
                ):
                    raise ValueError("unknown flavor or route")
                if space and expected in check_ordinals:
                    point = (
                        int(row[1]),
                        d["foods"][int(row[2])]["id"],
                        tuple(d["foods"][int(x)]["id"] for x in row[3:6] if x),
                        d["flavors"][int(row[6])],
                        d["routes"][int(row[7])],
                    )
                    if point != space.point(expected):
                        raise ValueError(
                            "materialized design point differs from ordinal definition"
                        )
                    checked_points += 1
                expected += 1
                count += 1
        if count != entry["rows"] or expected != entry["stop"]:
            raise ValueError("shard count mismatch")
    if expected != m["total"]:
        raise ValueError("total count mismatch")
    return {
        "rows_verified": expected,
        "shards_verified": len(m["shards"]),
        "decoded_points_matched": checked_points,
    }
