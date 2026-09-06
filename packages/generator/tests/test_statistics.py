import math
import unittest

from recipeweave_generator.statistics import (
    analyze,
    compare_proportions,
    newcombe_difference_interval,
    wilson_interval,
)


class StatisticsTest(unittest.TestCase):
    def test_wilson_interval_handles_extreme_counts(self):
        lo, hi = wilson_interval(0, 400)
        self.assertEqual(lo, 0.0)
        self.assertGreater(hi, 0.0)
        lo, hi = wilson_interval(400, 400)
        self.assertLess(lo, 1.0)
        self.assertEqual(hi, 1.0)

    def test_newcombe_hybrid_score_interval(self):
        lo, hi = newcombe_difference_interval(40, 100, 20, 100)
        a_lo, a_hi = wilson_interval(40, 100)
        b_lo, b_hi = wilson_interval(20, 100)
        difference = 0.40 - 0.20
        self.assertAlmostEqual(lo, difference - math.sqrt((0.40 - a_lo) ** 2 + (b_hi - 0.20) ** 2))
        self.assertAlmostEqual(hi, difference + math.sqrt((a_hi - 0.40) ** 2 + (0.20 - b_lo) ** 2))

    def test_newcombe_near_boundaries_fixture(self):
        # 手計算で独立に求めたハイブリッド式の期待値。従来の端点の単純な差分では、
        # 結果に無視できない差が生じる例を使う。
        lo, hi = newcombe_difference_interval(1, 400, 399, 400)
        a_lo, a_hi = wilson_interval(1, 400)
        b_lo, b_hi = wilson_interval(399, 400)
        d = 1 / 400 - 399 / 400
        expected_lo = max(-1.0, d - math.sqrt((1 / 400 - a_lo) ** 2 + (b_hi - 399 / 400) ** 2))
        expected_hi = min(1.0, d + math.sqrt((a_hi - 1 / 400) ** 2 + (399 / 400 - b_lo) ** 2))
        self.assertAlmostEqual(lo, expected_lo)
        self.assertAlmostEqual(hi, expected_hi)

    def test_analyze_counts_endpoints_and_comparison(self):
        samples = [
            {"id": "b0", "cohort": "baseline"},
            {"id": "b1", "cohort": "baseline"},
            {"id": "r0", "cohort": "revised"},
            {"id": "r1", "cohort": "revised"},
        ]
        a = [
            {"id": "b0", "verdict": "pass"},
            {"id": "b1", "verdict": "uncertain"},
            {"id": "r0", "verdict": "pass"},
            {"id": "r1", "verdict": "fail"},
        ]
        b = [
            {"id": "b0", "verdict": "pass"},
            {"id": "b1", "verdict": "fail"},
            {"id": "r0", "verdict": "uncertain"},
            {"id": "r1", "verdict": "fail"},
        ]
        report = analyze(samples, a, b)
        base = report["cohorts"]["baseline"]
        self.assertEqual(base["n"], 2)
        self.assertEqual(base["primary"]["count"], 1)
        self.assertEqual(base["either_pass"]["count"], 1)
        self.assertEqual(base["agreement"]["count"], 1)
        self.assertAlmostEqual(base["judge_a_pass"]["estimate"], 0.5)
        self.assertAlmostEqual(base["cohen_kappa"], 1 / 3)
        self.assertIn("primary", report["comparisons"])
        self.assertEqual(report["comparison_cohorts"], ["baseline", "revised"])
        self.assertFalse(report["method"]["finite_population_correction_applied"])
        self.assertEqual(report["population_by_cohort"]["baseline"], 25_171_059_494)
        self.assertEqual(report["population_by_cohort"]["revised"], 12_069_539)

    def test_kappa_undefined_without_marginal_variation(self):
        samples = [{"id": "x", "cohort": "pilot"}, {"id": "y", "cohort": "pilot"}]
        ratings = [{"id": "x", "verdict": "pass"}, {"id": "y", "verdict": "pass"}]
        report = analyze(samples, ratings, ratings)
        self.assertIsNone(report["cohorts"]["pilot"]["cohen_kappa"])
        self.assertIn("undefined", report["cohorts"]["pilot"]["cohen_kappa_note"])

    def test_validation_rejects_duplicate_unknown_and_missing(self):
        samples = [{"id": "x", "cohort": "pilot"}]
        good = [{"id": "x", "verdict": "pass"}]
        with self.assertRaises(ValueError):
            analyze(samples + [{"id": "x", "cohort": "pilot"}], good, good)
        with self.assertRaises(ValueError):
            analyze(samples, [{"id": "y", "verdict": "pass"}], good)
        with self.assertRaises(ValueError):
            analyze(samples, [{"id": "x", "verdict": "maybe"}], good)
        with self.assertRaises(ValueError):
            analyze(samples, [], good)

    def test_z_test_degenerate_case_is_defined(self):
        result = compare_proportions(0, 10, 0, 10)
        self.assertEqual(result["p_value"], 1.0)
        self.assertEqual(result["z"], 0.0)
        self.assertTrue(all(math.isfinite(x) for x in result["ci95"]))


if __name__ == "__main__":
    unittest.main()
