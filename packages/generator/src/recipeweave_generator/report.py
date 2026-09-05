"""Reproducible confirmation-study report.

Run from the repository root with::

    uv run python -m recipeweave_generator.report

The command validates the frozen design and sampled ordinals before joining
the four blinded judge result files.  It writes ``analysis.json`` and
``evidence.json`` beside the frozen confirmation inputs.  It never resamples,
changes labels, or calls a model.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .space import Space
from .statistics import analyze, compare_proportions

# v2 has 25,171,059,494 generated points; the confirmation population
# excludes the 100 pilot ordinals and is therefore 25,171,059,394.
BASELINE_FULL_POPULATION = 25_171_059_494
BASELINE_POPULATION = BASELINE_FULL_POPULATION - 100
REVISED_POPULATION = 12_069_539
EXPECTED_DEFINITION_DIGESTS = {
    "baseline": "486f8f288d2c26241959cbb70216aab27a712f0a7ff39f3a9783820924339782",
    "revised": "495dc6b22638ff029c75913a13aef616c425049eacddc6389a6a26257e56da36",
}
EXPECTED_PROTOCOL_SHA256 = "641c8cf2917cd5a1a9c1ef5421c268b571cd731286a3e3a3cf5ee085b3d7d465"
EXPECTED_SAMPLE_N = 400
VERDICTS = {"pass", "uncertain", "fail"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_ordinals(space: Space, seed: int, n: int, excluded: set[int]) -> set[int]:
    """Reproduce experiment.prepare's rejection sampler without resampling."""

    rng = random.Random(seed)
    selected: list[int] = []
    used = set(excluded)
    while len(selected) < n:
        ordinal = rng.randrange(space.total)
        if ordinal in used:
            continue
        used.add(ordinal)
        selected.append(ordinal)
    return set(selected)


def _validate_design(
    root: Path, confirmation: Path
) -> tuple[dict[str, Any], dict[str, Space], dict[str, Any]]:
    design = _read_json(confirmation / "design.json")
    if set(design.get("cohorts", {})) != {"baseline", "revised"}:
        raise ValueError("design must contain exactly baseline and revised cohorts")
    if design.get("method") != "SRS without replacement":
        raise ValueError("unexpected sampling method")
    if design.get("judge_slots_per_item") != 2 or design.get("judge_model") != "gpt-5.6-luna":
        raise ValueError("unexpected judge protocol")
    protocol_sha = _sha256(root / "experiments/PROTOCOL.md")
    if protocol_sha != design.get("protocol_sha256") or protocol_sha != EXPECTED_PROTOCOL_SHA256:
        raise ValueError("protocol hash does not match the frozen design")
    spaces = {
        "baseline": Space.load(root / "data/catalog/v2_baseline.json"),
        "revised": Space.load(root / "data/catalog/v3_reviewed.json"),
    }
    expected_population = {"baseline": BASELINE_POPULATION, "revised": REVISED_POPULATION}
    for cohort, space in spaces.items():
        frozen = design["cohorts"][cohort]
        if (
            space.digest != frozen.get("definition_sha256")
            or space.digest != EXPECTED_DEFINITION_DIGESTS[cohort]
        ):
            raise ValueError(f"{cohort} definition digest does not match frozen design")
        if (
            frozen.get("n") != EXPECTED_SAMPLE_N
            or frozen.get("population") != expected_population[cohort]
        ):
            raise ValueError(f"{cohort} population or sample size changed")
    if len(design.get("pilot_excluded_from_baseline", [])) != 100:
        raise ValueError("baseline pilot exclusion list must contain 100 ordinals")
    if len(set(design["pilot_excluded_from_baseline"])) != 100:
        raise ValueError("baseline pilot exclusion list contains duplicates")
    return design, spaces, {"protocol_sha256": protocol_sha, "populations": expected_population}


def _validate_samples(
    confirmation: Path,
    design: dict[str, Any],
    spaces: dict[str, Space],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = _read_json(confirmation / "samples_key.json")
    if not isinstance(rows, list) or len(rows) != 2 * EXPECTED_SAMPLE_N:
        raise ValueError("samples_key.json must contain 800 rows")
    expected_ids = {f"C{i:04d}" for i in range(800)}
    ids = [row.get("id") for row in rows]
    if set(ids) != expected_ids or len(ids) != len(set(ids)):
        raise ValueError("sample IDs must be exactly C0000..C0799")
    by_cohort: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        cohort = row.get("cohort")
        if cohort not in spaces:
            raise ValueError(f"unknown sample cohort: {cohort!r}")
        by_cohort[cohort].append(row)
        if (
            not isinstance(row.get("ordinal"), int)
            or not 0 <= row["ordinal"] < spaces[cohort].total
        ):
            raise ValueError(f"ordinal outside {cohort} space: {row.get('ordinal')!r}")
        expected = spaces[cohort].describe(row["ordinal"])
        for field in ("structure", "main", "supports", "flavor", "route"):
            if row.get(field) != expected[field]:
                raise ValueError(f"sample {row['id']} disagrees with frozen definition at {field}")
    excluded = set(design["pilot_excluded_from_baseline"])
    for cohort in spaces:
        cohort_rows = by_cohort[cohort]
        if len(cohort_rows) != EXPECTED_SAMPLE_N:
            raise ValueError(f"{cohort} must contain 400 rows")
        ordinals = [row["ordinal"] for row in cohort_rows]
        if len(set(ordinals)) != EXPECTED_SAMPLE_N:
            raise ValueError(f"{cohort} sample ordinals are duplicated")
        if cohort == "baseline" and excluded.intersection(ordinals):
            raise ValueError("baseline confirmation sample contains pilot ordinal")
        expected = _expected_ordinals(
            spaces[cohort], design["cohorts"][cohort]["seed"], EXPECTED_SAMPLE_N,
            excluded if cohort == "baseline" else set(),
        )
        if set(ordinals) != expected:
            raise ValueError(f"{cohort} ordinals do not match frozen seed")
    rows_by_id = {row["id"]: row for row in rows}
    for blind_name in ("blind_0.json", "blind_1.json"):
        blind_rows = _read_json(confirmation / blind_name)
        if not isinstance(blind_rows, list) or len(blind_rows) != EXPECTED_SAMPLE_N:
            raise ValueError(f"{blind_name} must contain 400 rows")
        blind_ids = [row.get("id") for row in blind_rows]
        if len(blind_ids) != len(set(blind_ids)) or not set(blind_ids) <= set(rows_by_id):
            raise ValueError(f"{blind_name} has duplicate or unknown IDs")
        for row in blind_rows:
            expected = {
                field: rows_by_id[row["id"]][field]
                for field in ("structure", "main", "supports", "flavor", "route", "id")
            }
            if row != expected:
                raise ValueError(f"{blind_name} does not match sample key for {row['id']}")
    blind_ids = [
        row["id"]
        for name in ("blind_0.json", "blind_1.json")
        for row in _read_json(confirmation / name)
    ]
    if set(blind_ids) != set(rows_by_id) or len(blind_ids) != len(set(blind_ids)):
        raise ValueError("blinded inputs do not exactly partition the sample key")
    return rows, {
        "n": len(rows),
        "ids_sha256": hashlib.sha256("\n".join(ids).encode()).hexdigest(),
        "by_cohort": {cohort: len(by_cohort[cohort]) for cohort in spaces},
        "ordinals_match_frozen_seeds": True,
        "baseline_excludes_pilot": True,
        "blinded_inputs_match_sample_key": True,
    }


def _validate_ratings(
    confirmation: Path, sample_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    sample_ids = {row["id"] for row in sample_rows}
    rating_files = {
        "judge_a": [confirmation / "judge_a0.json", confirmation / "judge_a1.json"],
        "judge_b": [confirmation / "judge_b0.json", confirmation / "judge_b1.json"],
    }
    combined: dict[str, list[dict[str, Any]]] = {}
    evidence: dict[str, Any] = {"files": {}}
    for judge, paths in rating_files.items():
        rows: list[dict[str, Any]] = []
        for path in paths:
            part = _read_json(path)
            if not isinstance(part, list) or len(part) != EXPECTED_SAMPLE_N:
                raise ValueError(f"{path.name} must contain 400 ratings")
            ids = [row.get("id") for row in part]
            if len(ids) != len(set(ids)) or not set(ids) <= sample_ids:
                raise ValueError(f"{path.name} has duplicate or unknown IDs")
            if any(row.get("verdict") not in VERDICTS for row in part):
                raise ValueError(f"{path.name} has an unknown verdict")
            evidence["files"][path.name] = {
                "sha256": _sha256(path), "rows": len(part), "judge": judge
            }
            rows.extend(part)
        ids = [row["id"] for row in rows]
        if set(ids) != sample_ids or len(ids) != len(set(ids)):
            raise ValueError(f"{judge} ratings do not exactly cover all samples")
        combined[judge] = rows
    evidence["coverage"] = {judge: len(rows) for judge, rows in combined.items()}
    evidence["model"] = "gpt-5.6-luna"
    evidence["actual_model"] = "gpt-5.6-luna"
    evidence["workers_per_item"] = 2
    evidence["human_results"] = 0
    evidence["human_labels"] = 0
    evidence["human_reviewed"] = False
    return combined["judge_a"], combined["judge_b"], evidence


def _template_breakdown(
    samples: list[dict[str, Any]], ratings_a: list[dict[str, Any]], ratings_b: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    a = {row["id"]: row["verdict"] for row in ratings_a}
    b = {row["id"]: row["verdict"] for row in ratings_b}
    grouped: Counter[tuple[str, str]] = Counter()
    passes: Counter[tuple[str, str]] = Counter()
    for row in samples:
        key = (row["cohort"], row["structure"])
        grouped[key] += 1
        passes[key] += a[row["id"]] == "pass" and b[row["id"]] == "pass"
    return [
        {"cohort": cohort, "template": structure, "n": grouped[(cohort, structure)],
         "both_pass": passes[(cohort, structure)],
         "both_pass_rate": passes[(cohort, structure)] / grouped[(cohort, structure)]}
        for cohort, structure in sorted(grouped)
    ]


def build_report(root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    root = (root or Path.cwd()).resolve()
    confirmation = root / "experiments/confirmation"
    design, spaces, design_evidence = _validate_design(root, confirmation)
    samples, sample_evidence = _validate_samples(confirmation, design, spaces)
    ratings_a, ratings_b, rating_evidence = _validate_ratings(confirmation, samples)
    sample_input = [{"id": row["id"], "cohort": row["cohort"]} for row in samples]
    report = analyze(
        sample_input,
        ratings_a,
        ratings_b,
        alpha=design["alpha"],
        population=design_evidence["populations"],
    )
    # Present the confirmatory effect in the policy direction: revised minus
    # baseline.  The generic analyzer keeps cohort order deterministic, but a
    # positive improvement is the readable and pre-specified report contrast.
    revised = report["cohorts"]["revised"]
    baseline = report["cohorts"]["baseline"]
    endpoint_counts = {
        "primary": (revised["primary"], baseline["primary"]),
        "either_pass": (revised["either_pass"], baseline["either_pass"]),
        "agreement": (revised["agreement"], baseline["agreement"]),
        "judge_a_pass": (revised["judge_a_pass"], baseline["judge_a_pass"]),
        "judge_b_pass": (revised["judge_b_pass"], baseline["judge_b_pass"]),
    }
    report["comparisons"] = {
        endpoint: compare_proportions(
            revised_measure["count"], revised_measure["n"],
            baseline_measure["count"], baseline_measure["n"],
            alpha=design["alpha"],
        )
        for endpoint, (revised_measure, baseline_measure) in endpoint_counts.items()
    }
    report["comparison"] = report["comparisons"]
    report["comparison_cohorts"] = ["revised", "baseline"]
    report["comparison_direction"] = "revised minus baseline"
    report["template_breakdown"] = _template_breakdown(samples, ratings_a, ratings_b)
    report["validation"] = {**design_evidence, **sample_evidence}
    manifest = _read_json(root / "data/exports/v3/manifest.json")
    normalization = _read_json(root / "data/catalog/normalization.json")
    report["catalog"] = {
        "source_foods": normalization["source_foods"],
        "culinary_identities": normalization["culinary_identities"],
        "active_primary_support_identities": normalization["active_primary_support_identities"],
        "templates": (
            normalization["templates"]
            if "templates" in normalization
            else len(normalization["counts_by_template"])
        ),
        "definition_sha256": normalization["definition_sha256"],
    }
    report["export"] = {
        "definition_sha256": manifest["definition_sha256"],
        "total_hypotheses": manifest["total"],
        "status": manifest["status"],
        "shards": len(manifest["shards"]),
        "compressed_bytes": sum(shard["bytes"] for shard in manifest["shards"]),
    }
    evidence = {
        "schema_version": 1,
        "study": "RecipeWeave confirmation",
        "design_sha256": _sha256(confirmation / "design.json"),
        "protocol_sha256": design_evidence["protocol_sha256"],
        "samples_key_sha256": _sha256(confirmation / "samples_key.json"),
        "blinded_inputs": {
            name: {
                "sha256": _sha256(confirmation / name),
                "rows": len(_read_json(confirmation / name)),
            }
            for name in ("blind_0.json", "blind_1.json")
        },
        "ratings": rating_evidence,
        "validation": {**sample_evidence, "definition_digests": EXPECTED_DEFINITION_DIGESTS},
        "judge_model": "gpt-5.6-luna",
        "actual_model": "gpt-5.6-luna",
        "workers_per_item": 2,
        "human_results": 0,
        "human_labels": 0,
        "human_reviewed": False,
        "all_results_present": True,
    }
    return report, evidence


def main() -> None:
    root = Path.cwd()
    report, evidence = build_report(root)
    confirmation = root / "experiments/confirmation"
    (confirmation / "analysis.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    (confirmation / "evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n"
    )
    primary = report["cohorts"]
    print(json.dumps({
        "analysis": str(confirmation / "analysis.json"),
        "evidence": str(confirmation / "evidence.json"),
        "baseline_both_pass": primary["baseline"]["primary"],
        "revised_both_pass": primary["revised"]["primary"],
        "primary_comparison": report["comparisons"]["primary"],
        "validation": report["validation"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
