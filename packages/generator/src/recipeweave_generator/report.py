"""再現可能な検証実験の報告を生成する。

リポジトリのルートから次を実行する::

    uv run python -m recipeweave_generator.report

固定した実験設計と抽出済みの通し番号を検証してから、盲検化された評価結果の
4ファイルを結合する。固定済みの検証入力と同じ場所へ ``analysis.json`` と
``evidence.json`` を出力する。再抽出、判定ラベルの変更、モデルの呼び出しは行わない。
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

# v2の生成点は25,171,059,494件。検証用の母集団は予備実験の通し番号100件を除くため、
# 25,171,059,394件となる。
BASELINE_FULL_POPULATION = 25_171_059_494
BASELINE_POPULATION = BASELINE_FULL_POPULATION - 100
REVISED_POPULATION = 12_069_539
EXPECTED_DEFINITION_DIGESTS = {
    "baseline": "486f8f288d2c26241959cbb70216aab27a712f0a7ff39f3a9783820924339782",
    "revised": "495dc6b22638ff029c75913a13aef616c425049eacddc6389a6a26257e56da36",
}
EXPECTED_PROTOCOL_SHA256 = "641c8cf2917cd5a1a9c1ef5421c268b571cd731286a3e3a3cf5ee085b3d7d465"
# 記録済みの検証実行に対して、事後的に整合性確認用のハッシュを固定する。
# これらは、この報告が受け入れる成果物を特定するための値であり、
# 評価前に実験設計が事前登録されていたことを示す証拠ではない。
EXPECTED_DESIGN_SHA256 = "a42e75c6a4bf738dcb5d36146fc9096542b27738c73376c8449d36d808632bf9"
EXPECTED_PILOT_DESIGN_SHA256 = "3ac09c0ecbcb25ba37490e6e0481f48be4eb891669e27cd64c477c3babeef6ad"
EXPECTED_SAMPLE_N = 400
VERDICTS = {"pass", "uncertain", "fail"}
DECLARED_JUDGE_MODEL = "gpt-5.6-luna"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_ordinals(space: Space, seed: int, n: int, excluded: set[int]) -> set[int]:
    """再抽出は行わず、experiment.prepareの棄却抽出を再現する。"""

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
    design_sha = _sha256(confirmation / "design.json")
    if design_sha != EXPECTED_DESIGN_SHA256:
        raise ValueError("confirmation design hash does not match retrospective integrity pin")
    if set(design.get("cohorts", {})) != {"baseline", "revised"}:
        raise ValueError("design must contain exactly baseline and revised cohorts")
    if (
        design.get("version") != 1
        or design.get("primary_endpoint") != "both_pass"
        or design.get("alpha") != 0.05
    ):
        raise ValueError("unexpected frozen confirmation design fields")
    if design.get("method") != "SRS without replacement":
        raise ValueError("unexpected sampling method")
    if design.get("judge_slots_per_item") != 2 or design.get("judge_model") != DECLARED_JUDGE_MODEL:
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
    pilot = _read_json(root / "experiments/pilot/design.json")
    pilot_sha = _sha256(root / "experiments/pilot/design.json")
    if pilot_sha != EXPECTED_PILOT_DESIGN_SHA256:
        raise ValueError("pilot design hash does not match retrospective integrity pin")
    pilot_ordinals = pilot.get("ordinals")
    if (
        pilot.get("n") != 100
        or pilot.get("sampling") != "simple random without replacement"
        or not isinstance(pilot_ordinals, list)
        or len(pilot_ordinals) != 100
        or any(
            not isinstance(ordinal, int)
            or isinstance(ordinal, bool)
            or not 0 <= ordinal < spaces["baseline"].total
            for ordinal in pilot_ordinals
        )
        or len(set(pilot_ordinals)) != 100
    ):
        raise ValueError("pilot design ordinals are invalid")
    excluded = design.get("pilot_excluded_from_baseline")
    if not isinstance(excluded, list) or len(excluded) != 100:
        raise ValueError("baseline pilot exclusion list must contain 100 ordinals")
    if any(
        not isinstance(ordinal, int)
        or isinstance(ordinal, bool)
        or not 0 <= ordinal < spaces["baseline"].total
        for ordinal in excluded
    ):
        raise ValueError("baseline pilot exclusion list contains an out-of-range ordinal")
    if len(set(excluded)) != 100:
        raise ValueError("baseline pilot exclusion list contains duplicates")
    if set(excluded) != set(pilot_ordinals):
        raise ValueError("baseline pilot exclusion list does not match pilot design")
    return design, spaces, {
        "protocol_sha256": protocol_sha,
        "design_sha256": design_sha,
        "pilot_design_sha256": pilot_sha,
        "design_hash_status": (
            "retrospectively pinned to baseline evidence; preregistration not established"
        ),
        "populations": expected_population,
    }


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
        "blinding": {
            "status": "limited",
            "cohort_field_hidden": True,
            "ordinal_field_hidden": True,
            "algorithm_name_field_hidden": True,
            "cohort_inference_from_structure_possible": (
                {
                    row["structure"]
                    for row in rows
                    if row["cohort"] == "baseline"
                }
                != {
                    row["structure"]
                    for row in rows
                    if row["cohort"] == "revised"
                }
            ),
            "limitation": (
                "structure labels remain visible and may reveal cohort or algorithm"
            ),
        },
    }


def _validate_ratings(
    confirmation: Path, sample_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    sample_ids = {row["id"] for row in sample_rows}
    blind_ids_by_shard = {
        f"blind_{shard}": [
            row["id"] for row in _read_json(confirmation / f"blind_{shard}.json")
        ]
        for shard in ("0", "1")
    }
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
            shard = path.stem[-1]
            if set(ids) != set(blind_ids_by_shard[f"blind_{shard}"]):
                raise ValueError(f"{path.name} IDs do not match blind_{shard}.json")
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
    evidence["model"] = DECLARED_JUDGE_MODEL
    evidence["declared_model"] = DECLARED_JUDGE_MODEL
    evidence["actual_model"] = None
    evidence["provenance_status"] = (
        "declared model retained; execution metadata and prompt/context hashes are absent"
    )
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
    # 検証する効果は、方針に沿って改訂版から従来版を引いた差として示す。
    # 汎用の分析器では群の順序を決定的に保つが、この報告では改善を正で表す
    # 事前定義の比較方向を使う。
    revised = report["cohorts"]["revised"]
    baseline = report["cohorts"]["baseline"]
    endpoint_counts = {
        "primary": (revised["primary"], baseline["primary"]),
        "either_pass": (revised["either_pass"], baseline["either_pass"]),
        "agreement": (revised["agreement"], baseline["agreement"]),
        "judge_a_pass": (revised["judge_a_pass"], baseline["judge_a_pass"]),
        "judge_b_pass": (revised["judge_b_pass"], baseline["judge_b_pass"]),
    }
    comparisons: dict[str, Any] = {}
    for endpoint, (revised_measure, baseline_measure) in endpoint_counts.items():
        comparison = compare_proportions(
            revised_measure["count"], revised_measure["n"],
            baseline_measure["count"], baseline_measure["n"],
            alpha=design["alpha"],
        )
        if endpoint != "primary":
            comparison.pop("reject", None)
            comparison["inference"] = "exploratory; no multiplicity-adjusted decision"
        comparisons[endpoint] = comparison
    report["comparisons"] = comparisons
    report["comparison"] = report["comparisons"]
    report["comparison_cohorts"] = ["revised", "baseline"]
    report["comparison_direction"] = "revised minus baseline"
    report["template_breakdown"] = _template_breakdown(samples, ratings_a, ratings_b)
    report["validation"] = {**design_evidence, **sample_evidence}
    report["method"]["blinding"] = sample_evidence["blinding"]
    report["method"]["secondary_inference"] = (
        "exploratory only; no multiplicity-adjusted confirmatory decision"
    )
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
        "judge_model": DECLARED_JUDGE_MODEL,
        "declared_model": DECLARED_JUDGE_MODEL,
        "actual_model": None,
        "provenance_status": (
            "declared model retained; execution metadata and prompt/context hashes are absent"
        ),
        "blinding": sample_evidence["blinding"],
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
