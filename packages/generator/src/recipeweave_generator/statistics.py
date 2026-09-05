"""Statistical summaries for two independent judge ratings.

The unit of analysis is a sampled design point.  Each point is rated by two
judges with one of ``pass``, ``uncertain`` or ``fail``.  The primary binary
endpoint is deliberately strict: both judges must say ``pass``.  This module
does not attempt to calibrate either judge against an external gold standard;
its intervals describe the sampled, model-judged population.

Only the Python standard library is used.  Proportions use unweighted SRS
Wilson score intervals (95 percent by default).  Since the baseline
RecipeWeave population is 25,171,059,494 (the revised population is tracked
separately) and the planned samples are 400, the finite
population correction is negligible and is intentionally not applied.  For a
pre-specified comparison, the difference interval is the
Newcombe hybrid score interval built from the two Wilson intervals.  The hypothesis test
is the two-sided pooled two-proportion z test at alpha=.05; no comparison is
selected from its observed result.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from statistics import NormalDist
from typing import Any

VERDICTS = ("pass", "uncertain", "fail")
DEFAULT_Z = NormalDist().inv_cdf(0.975)
DEFAULT_ALPHA = 0.05
RECIPEWEAVE_POPULATION = 25_171_059_494
REVISED_POPULATION = 12_069_539
DEFAULT_POPULATIONS = {"baseline": RECIPEWEAVE_POPULATION, "revised": REVISED_POPULATION}
WORST_CASE_N_5PP = math.ceil(DEFAULT_Z * DEFAULT_Z * 0.25 / (0.05 * 0.05))


def _check_count(x: int, n: int) -> None:
    if not isinstance(x, int) or isinstance(x, bool) or not 0 <= x <= n:
        raise ValueError(f"count must be an integer between 0 and n ({n})")


def wilson_interval(count: int, n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Return a Wilson score interval for an unweighted binary proportion."""

    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ValueError("n must be a positive integer")
    _check_count(count, n)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    z = NormalDist().inv_cdf((1.0 + confidence) / 2.0)
    p = count / n
    z2 = z * z
    denominator = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denominator
    half = z / denominator * math.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n))
    lower, upper = max(0.0, center - half), min(1.0, center + half)
    # Preserve exact endpoint conventions despite floating-point roundoff.
    if count == 0:
        lower = 0.0
    if count == n:
        upper = 1.0
    return lower, upper


def newcombe_difference_interval(
    count_a: int,
    n_a: int,
    count_b: int,
    n_b: int,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Return the Newcombe hybrid score difference interval ``p_a - p_b``.

    This is Newcombe's hybrid score interval.  Each binomial proportion uses
    its Wilson limits, and the two resulting score distances are combined in
    quadrature, including when an observed proportion is near 0 or 1.
    """

    a_lo, a_hi = wilson_interval(count_a, n_a, confidence)
    b_lo, b_hi = wilson_interval(count_b, n_b, confidence)
    p_a, p_b = count_a / n_a, count_b / n_b
    difference = p_a - p_b
    lower = difference - math.sqrt((p_a - a_lo) ** 2 + (b_hi - p_b) ** 2)
    upper = difference + math.sqrt((a_hi - p_a) ** 2 + (p_b - b_lo) ** 2)
    return max(-1.0, lower), min(1.0, upper)


def _measure(count: int, n: int, confidence: float) -> dict[str, Any]:
    lo, hi = wilson_interval(count, n, confidence)
    estimate = count / n
    return {
        "count": count,
        "n": n,
        "estimate": estimate,
        "proportion": estimate,
        "ci95": [lo, hi],
        "ci": [lo, hi],
    }


def compare_proportions(
    count_a: int,
    n_a: int,
    count_b: int,
    n_b: int,
    *,
    alpha: float = DEFAULT_ALPHA,
    confidence: float = 0.95,
) -> dict[str, Any]:
    """Compare two independent binary endpoints using a pooled z test."""

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if not isinstance(n_a, int) or not isinstance(n_b, int) or n_a <= 0 or n_b <= 0:
        raise ValueError("sample sizes must be positive integers")
    _check_count(count_a, n_a)
    _check_count(count_b, n_b)
    p_a, p_b = count_a / n_a, count_b / n_b
    difference = p_a - p_b
    pooled = (count_a + count_b) / (n_a + n_b)
    variance = pooled * (1.0 - pooled) * (1.0 / n_a + 1.0 / n_b)
    if variance == 0:
        z_stat = 0.0 if difference == 0 else math.copysign(math.inf, difference)
        p_value = 1.0 if difference == 0 else 0.0
    else:
        z_stat = difference / math.sqrt(variance)
        p_value = math.erfc(abs(z_stat) / math.sqrt(2.0))
    lo, hi = newcombe_difference_interval(count_a, n_a, count_b, n_b, confidence)
    return {
        "count_a": count_a,
        "n_a": n_a,
        "count_b": count_b,
        "n_b": n_b,
        "estimate_a": p_a,
        "estimate_b": p_b,
        "difference": difference,
        "ci95": [lo, hi],
        "ci": [lo, hi],
        "method": "Newcombe hybrid score interval (Wilson, no continuity correction)",
        "test": "two-sided pooled two-proportion z test",
        "alpha": alpha,
        "z": z_stat,
        "z_statistic": z_stat,
        "p_value": p_value,
        "reject": p_value < alpha,
    }


def _records(records: Sequence[Mapping[str, Any]], label: str) -> list[Mapping[str, Any]]:
    if isinstance(records, str | bytes) or not isinstance(records, Sequence):
        raise ValueError(f"{label} must be a sequence of records")
    out = list(records)
    if not out:
        raise ValueError(f"{label} must not be empty")
    if any(not isinstance(row, Mapping) for row in out):
        raise ValueError(f"{label} records must be mappings")
    return out


def _rating_map(
    ratings: Sequence[Mapping[str, Any]], label: str, sample_ids: set[Any]
) -> dict[Any, str]:
    rows = _records(ratings, label)
    out: dict[Any, str] = {}
    for row in rows:
        if "id" not in row:
            raise ValueError(f"{label} record is missing id")
        ident = row["id"]
        try:
            if ident in out:
                raise ValueError(f"duplicate id in {label}: {ident!r}")
            out[ident] = row.get("verdict")
        except TypeError as exc:
            raise ValueError(f"unhashable id in {label}: {ident!r}") from exc
        if out[ident] not in VERDICTS:
            raise ValueError(f"unknown verdict in {label}: {out[ident]!r}")
        if ident not in sample_ids:
            raise ValueError(f"unknown id in {label}: {ident!r}")
    missing = sample_ids - out.keys()
    if missing:
        raise ValueError(f"missing {label} ratings for ids: {sorted(missing, key=repr)!r}")
    if len(out) != len(sample_ids):
        raise ValueError(f"{label} does not exactly cover samples")
    return out


def _summary(rows: list[tuple[str, str]], confidence: float) -> dict[str, Any]:
    n = len(rows)
    a = Counter(x for x, _ in rows)
    b = Counter(y for _, y in rows)
    cells = Counter(f"{x}/{y}" for x, y in rows)
    both = sum(x == "pass" and y == "pass" for x, y in rows)
    either = sum(x == "pass" or y == "pass" for x, y in rows)
    agreement = sum(x == y for x, y in rows)
    primary = _measure(both, n, confidence)
    secondary = {
        "either_pass": _measure(either, n, confidence),
        "agreement": _measure(agreement, n, confidence),
        "judge_a_pass": _measure(a["pass"], n, confidence),
        "judge_b_pass": _measure(b["pass"], n, confidence),
    }
    marginal = {"judge_a": secondary["judge_a_pass"], "judge_b": secondary["judge_b_pass"]}
    expected = sum((a[v] / n) * (b[v] / n) for v in VERDICTS)
    observed = agreement / n
    # When both judges use one category for every row, chance agreement is 1
    # and kappa has no variation from which to be estimated.
    kappa = None if expected == 1.0 else (observed - expected) / (1.0 - expected)
    result: dict[str, Any] = {
        "n": n,
        "verdict_counts": {
            "judge_a": {v: a[v] for v in VERDICTS},
            "judge_b": {v: b[v] for v in VERDICTS},
        },
        "confusion_matrix": {x: {y: cells[f"{x}/{y}"] for y in VERDICTS} for x in VERDICTS},
        "primary": primary,
        "primary_endpoint": primary,
        "secondary": {
            **secondary,
            "cohen_kappa": kappa,
            "marginal_judge_pass": marginal,
            "cohen_kappa_note": "undefined: no marginal variation" if kappa is None else None,
        },
        "both_pass": primary,
        **secondary,
        "marginal_judge_pass": marginal,
        "marginaljudgepass": marginal,
        "cohen_kappa": kappa,
        "cohen_kappa_note": "undefined: no marginal variation" if kappa is None else None,
    }
    return result


def analyze(
    samples: Sequence[Mapping[str, Any]],
    ratings_a: Sequence[Mapping[str, Any]],
    ratings_b: Sequence[Mapping[str, Any]],
    *,
    confidence: float = 0.95,
    alpha: float = DEFAULT_ALPHA,
    population: int | Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """Validate ratings and return endpoint summaries grouped by cohort.

    If ``baseline`` and ``revised`` cohorts are present, that pair is the
    sole confirmatory comparison.  With exactly two other cohort names, that
    pair is compared as a convenience.  Additional cohorts (such as the
    development ``pilot``) are summarized but are never silently used to
    select a hypothesis comparison.
    """

    sample_rows = _records(samples, "samples")
    if not 0 < confidence < 1 or not 0 < alpha < 1:
        raise ValueError("confidence and alpha must be between 0 and 1")
    if population is None:
        populations: dict[str, int] = dict(DEFAULT_POPULATIONS)
    elif isinstance(population, Mapping):
        populations = dict(population)
    elif isinstance(population, int) and not isinstance(population, bool) and population > 0:
        populations = {}
    else:
        raise ValueError("population must be a positive integer or cohort mapping")
    if population is not None and isinstance(population, Mapping):
        if any(
            not isinstance(value, int) or isinstance(value, bool) or value <= 0
            for value in populations.values()
        ):
            raise ValueError("each cohort population must be a positive integer")
    sample_ids: set[Any] = set()
    sample_cohorts: dict[Any, Any] = {}
    for row in sample_rows:
        if "id" not in row or "cohort" not in row:
            raise ValueError("each sample must contain id and cohort")
        ident, cohort = row["id"], row["cohort"]
        try:
            if ident in sample_ids:
                raise ValueError(f"duplicate sample id: {ident!r}")
            sample_ids.add(ident)
            hash(cohort)
            sample_cohorts[ident] = cohort
        except TypeError as exc:
            raise ValueError(f"unhashable sample id or cohort: {ident!r}") from exc
    a = _rating_map(ratings_a, "ratings_a", sample_ids)
    b = _rating_map(ratings_b, "ratings_b", sample_ids)
    grouped: dict[Any, list[tuple[str, str]]] = {}
    for ident in sample_ids:
        grouped.setdefault(sample_cohorts[ident], []).append((a[ident], b[ident]))
    # Make output deterministic independent of set/dict insertion order.
    grouped = {key: grouped[key] for key in sorted(grouped, key=repr)}
    cohorts = {str(key): _summary(rows, confidence) for key, rows in grouped.items()}
    for name, summary in cohorts.items():
        if name in populations:
            summary["population"] = populations[name]
            summary["sampling_fraction"] = summary["n"] / populations[name]
    names = list(grouped)
    pair: tuple[Any, Any] | None = None
    by_name = {str(k): k for k in names}
    if "baseline" in by_name and "revised" in by_name:
        pair = (by_name["baseline"], by_name["revised"])
    elif len(names) == 2:
        pair = (names[0], names[1])
    comparisons: dict[str, Any] = {}
    if pair is not None:
        left, right = pair
        left_rows, right_rows = grouped[left], grouped[right]
        for endpoint in ("primary", "either_pass", "agreement", "judge_a_pass", "judge_b_pass"):
            if endpoint == "primary":
                x = sum(a == "pass" and b == "pass" for a, b in left_rows)
                y = sum(a == "pass" and b == "pass" for a, b in right_rows)
            elif endpoint == "either_pass":
                x = sum(a == "pass" or b == "pass" for a, b in left_rows)
                y = sum(a == "pass" or b == "pass" for a, b in right_rows)
            elif endpoint == "agreement":
                x = sum(a == b for a, b in left_rows)
                y = sum(a == b for a, b in right_rows)
            elif endpoint == "judge_a_pass":
                x = sum(a == "pass" for a, _ in left_rows)
                y = sum(a == "pass" for a, _ in right_rows)
            else:
                x = sum(b == "pass" for _, b in left_rows)
                y = sum(b == "pass" for _, b in right_rows)
            comparisons[endpoint] = compare_proportions(
                x, len(left_rows), y, len(right_rows), alpha=alpha, confidence=confidence
            )
    report = {
        "population": populations if populations else population,
        "population_by_cohort": populations,
        "n": len(sample_rows),
        "cohorts": cohorts,
        "comparisons": comparisons,
        "comparison": comparisons,
        "comparison_cohorts": [str(x) for x in pair] if pair is not None else None,
        "method": {
            "sampling": "simple random sampling without replacement",
            "confidence": confidence,
            "alpha": alpha,
            "wilson": "unweighted SRS Wilson score interval",
            "comparison_ci": "Newcombe hybrid score difference interval",
            "comparison_test": "two-sided pooled two-proportion z test",
            "finite_population_correction_applied": False,
            "finite_population_effect": (
                "negligible for planned n=400; finite-population correction is not applied"
            ),
            "finite_population_sampling_fraction_at_n400": {
                name: 400 / size for name, size in populations.items()
            },
            "worst_case_n_for_plus_minus_5pp": WORST_CASE_N_5PP,
            "approximate_worst_case_margin_at_n400": DEFAULT_Z * math.sqrt(0.25 / 400),
            "interpretation": (
                "confidence applies to the model-judged sampled population; "
                "shared model bias is not removed and two judges do not double n"
            ),
            "pilot": (
                "development pilot is summarized separately and is not used "
                "to select the confirmatory comparison"
            ),
        },
    }
    return report


__all__ = [
    "VERDICTS",
    "wilson_interval",
    "newcombe_difference_interval",
    "compare_proportions",
    "analyze",
]
