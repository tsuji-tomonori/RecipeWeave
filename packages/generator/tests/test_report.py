import json
import shutil
import tempfile
import unittest
from pathlib import Path

from recipeweave_generator.report import build_report

ROOT = Path(__file__).parents[3]


def copy_report_fixture() -> tempfile.TemporaryDirectory[str]:
    temporary = tempfile.TemporaryDirectory()
    root = Path(temporary.name)
    for relative in (
        "experiments/PROTOCOL.md",
        "experiments/pilot/design.json",
        "experiments/confirmation/design.json",
        "experiments/confirmation/samples_key.json",
        "experiments/confirmation/blind_0.json",
        "experiments/confirmation/blind_1.json",
        "experiments/confirmation/judge_a0.json",
        "experiments/confirmation/judge_a1.json",
        "experiments/confirmation/judge_b0.json",
        "experiments/confirmation/judge_b1.json",
        "data/catalog/v2_baseline.json",
        "data/catalog/v3_reviewed.json",
        "data/catalog/normalization.json",
        "data/exports/v3/manifest.json",
    ):
        source = ROOT / relative
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return temporary


class ReportTest(unittest.TestCase):
    def test_report_preserves_primary_and_honest_provenance_metadata(self):
        temporary = copy_report_fixture()
        self.addCleanup(temporary.cleanup)

        report, evidence = build_report(Path(temporary.name))

        self.assertEqual(report["cohorts"]["baseline"]["primary"]["count"], 164)
        self.assertEqual(report["cohorts"]["revised"]["primary"]["count"], 398)
        self.assertTrue(report["comparisons"]["primary"]["reject"])
        self.assertTrue(all("reject" not in report["comparisons"][name] for name in (
            "either_pass", "agreement", "judge_a_pass", "judge_b_pass"
        )))
        self.assertEqual(evidence["ratings"]["model"], "gpt-5.6-luna")
        self.assertEqual(evidence["ratings"]["declared_model"], "gpt-5.6-luna")
        self.assertIsNone(evidence["ratings"]["actual_model"])
        self.assertIn("execution metadata", evidence["ratings"]["provenance_status"])
        self.assertEqual(evidence["blinding"]["status"], "limited")
        self.assertTrue(evidence["blinding"]["cohort_inference_from_structure_possible"])
        self.assertIn("preregistration not established", report["validation"]["design_hash_status"])

    def test_changed_confirmation_design_is_rejected(self):
        temporary = copy_report_fixture()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "experiments/confirmation/design.json"
        design = json.loads(path.read_text())
        design["alpha"] = 0.10
        path.write_text(json.dumps(design))

        with self.assertRaisesRegex(ValueError, "design hash"):
            build_report(Path(temporary.name))

    def test_changed_pilot_design_is_rejected(self):
        temporary = copy_report_fixture()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "experiments/pilot/design.json"
        design = json.loads(path.read_text())
        design["ordinals"][0] += 1
        path.write_text(json.dumps(design))

        with self.assertRaisesRegex(ValueError, "pilot design hash"):
            build_report(Path(temporary.name))

    def test_rating_shard_must_match_blinded_input_shard(self):
        temporary = copy_report_fixture()
        self.addCleanup(temporary.cleanup)
        rating_path = Path(temporary.name) / "experiments/confirmation/judge_a0.json"
        other_path = Path(temporary.name) / "experiments/confirmation/judge_a1.json"
        ratings = json.loads(rating_path.read_text())
        other_ratings = json.loads(other_path.read_text())
        ratings[0], other_ratings[0] = other_ratings[0], ratings[0]
        rating_path.write_text(json.dumps(ratings))
        other_path.write_text(json.dumps(other_ratings))

        with self.assertRaisesRegex(ValueError, "IDs do not match blind_0"):
            build_report(Path(temporary.name))


if __name__ == "__main__":
    unittest.main()
