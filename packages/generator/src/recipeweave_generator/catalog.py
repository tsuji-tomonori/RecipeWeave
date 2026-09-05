"""Compile reviewed role allowlists. Unknown items fail closed, never guess by regex."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
from pathlib import Path
from typing import Any

from .export import atomic_json
from .space import Space, canonical


def compile_catalog(
    source: list[dict[str, Any]], policy: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    mapping: dict[str, str] = {}
    source_names = {row["name"] for row in source}
    for group in policy["aliases"]:
        for member in group["members"]:
            if member not in source_names:
                raise ValueError(f"unknown alias member: {member}")
            if member in mapping and mapping[member] != group["name"]:
                raise ValueError("ambiguous alias")
            mapping[member] = group["name"]
    identities: dict[str, dict[str, Any]] = {}
    variants = []
    for row in source:
        name = mapping.get(row["name"], row["name"])
        ident = "ingredient_" + hashlib.sha256(name.encode()).hexdigest()[:16]
        record = identities.setdefault(
            name, {"id": ident, "name": name, "source_ids": [], "availability": []}
        )
        record["source_ids"].append(row["id"])
        record["availability"].append(row["availability"])
        match = re.fullmatch(r"めんつゆ([234])倍", row["name"])
        variants.append(
            {
                "source_id": row["id"],
                "identity_id": ident,
                "name": row["name"],
                "state": row["state"],
                "unit": row["unit"],
                "availability": row["availability"],
                "concentration_multiplier": int(match[1]) if match else None,
                "conversion_reference": None,
            }
        )
    pools = {}
    excluded = []
    for name, members in policy["pools"].items():
        normalized = set(mapping.get(member, member) for member in members)
        if missing := normalized - identities.keys():
            raise ValueError(f"unknown pool members {name}: {missing}")
        pools[name] = {
            identities[n]["id"]: n
            for n in sorted(normalized)
            if policy["availability"] in identities[n]["availability"]
        }
        excluded.extend(
            {"pool": name, "name": n, "reason": "no_common_variant"}
            for n in sorted(normalized)
            if policy["availability"] not in identities[n]["availability"]
        )
    blocks = []
    for template in policy["templates"]:
        excludes = {mapping.get(n, n) for n in template["exclude_primary"]}
        primary = {i: n for i, n in pools[template["primary_pool"]].items() if n not in excludes}
        supports = dict(pools[template["support_pool"]])
        block = {
            "code": template["code"],
            "label": template["label"],
            "primary": primary,
            "supports": supports,
            "k": template["k"],
            "flavors": policy["flavors"][template["flavor_group"]],
            "routes": [template["route"]],
        }
        if cross := template.get("cross_pool"):
            other = pools[cross]
            # Each pair has a distinct culinary role, with symmetric identities deduplicated.
            pairs = {tuple(sorted((a, b))) for a, b in itertools.product(supports, other) if a != b}
            sets = {(x,) for x in supports} | pairs
            block["supports"] = supports | other
            block["support_sets"] = [list(x) for x in sorted(sets, key=lambda x: (len(x), x))]
        blocks.append(block)
    definition = {
        "version": policy["version"],
        "source_sha256": hashlib.sha256(canonical(source)).hexdigest(),
        "policy_sha256": hashlib.sha256(canonical(policy)).hexdigest(),
        "blocks": blocks,
        "scope": (
            "All candidates admitted by the explicit role and route policy; "
            "not all supermarket combinations"
        ),
    }
    space = Space(definition)
    active = set(space.names)
    report = {
        "variant_note": (
            "倍率表示を保持するが異なる商品の塩糖量や質量を推定しない。換算は商品版・根拠を確定後"
        ),
        "source_foods": len(source),
        "culinary_identities": len(identities),
        "active_primary_support_identities": len(active),
        "candidate_count": space.total,
        "templates": len(blocks),
        "definition_sha256": space.digest,
        "identities": sorted(identities.values(), key=lambda x: x["id"]),
        "variants": variants,
        "not_enumerated": [
            {
                "id": i["id"],
                "name": i["name"],
                "reason": "seasoning_or_unreviewed_role_or_noncommon; retained in catalog",
            }
            for i in identities.values()
            if i["id"] not in active
        ],
        "excluded_from_pools": excluded,
        "counts_by_template": [
            {"code": b["code"], "count": sum(s.count for s in space.segments if s.template == t)}
            for t, b in enumerate(blocks)
        ],
    }
    return definition, report


def compile_files(catalog_dir: Path) -> dict[str, Any]:
    definition, report = compile_catalog(
        json.loads((catalog_dir / "source_foods.json").read_text()),
        json.loads((catalog_dir / "policy.json").read_text()),
    )
    atomic_json(catalog_dir / "v3_reviewed.json", definition, compact=True)
    atomic_json(catalog_dir / "normalization.json", report, compact=True)
    return {
        k: v
        for k, v in report.items()
        if k not in {"identities", "variants", "not_enumerated", "excluded_from_pools"}
    }
