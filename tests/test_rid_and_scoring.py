import json
import tempfile
import unittest
from pathlib import Path

from src.evaluation.validity_checklists import ValidityScorer
from src.pipeline.generate_exp_b_scenarios import make_did
from src.pipeline.run_exp_c import prepare_precommitment


class ValidityScorerTests(unittest.TestCase):
    def test_score_writes_exp_a_compatible_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            scorer = ValidityScorer("DID", output_dir=tmpdir)
            scorer.score(
                [1, 1, 1, 1, 0],
                rater_id="rater_1",
                paper_id="paper_01",
                id_strategy_score=3,
                conclusion_score=1.0,
                effect_size_score=0.5,
                save=True,
            )

            score_file = Path(tmpdir) / "paper_01_rater_1.json"
            self.assertTrue(score_file.exists())

            payload = json.loads(score_file.read_text())
            self.assertEqual(payload["id_strategy_score"], 3)
            self.assertEqual(payload["conclusion_score"], 1.0)
            self.assertEqual(payload["effect_size_score"], 0.5)


class GenerateDidTests(unittest.TestCase):
    def test_make_did_treatment_starts_on_treat_period(self):
        df = make_did(
            n_units=2,
            n_periods=4,
            treat_frac=0.5,
            effect=1.0,
            treat_period=3,
            noise=0.0,
            panel_fe=False,
        )

        treated_period = df[(df["unit_id"] == 0) & (df["period"] == 3)].iloc[0]
        control_period = df[(df["unit_id"] == 1) & (df["period"] == 3)].iloc[0]

        self.assertEqual(int(treated_period["post"]), 1)
        self.assertEqual(int(treated_period["treat_x_post"]), 1)
        self.assertEqual(int(control_period["post"]), 1)
        self.assertEqual(int(control_period["treat_x_post"]), 0)

    def test_make_did_uses_fixed_unit_effects(self):
        df = make_did(
            n_units=6,
            n_periods=3,
            treat_frac=0.5,
            effect=0.0,
            treat_period=99,
            noise=0.0,
            panel_fe=True,
        )

        residual = df["y"] - 0.5 * df["treated"] - 0.4 * df["post"]
        unique_effects = residual.groupby(df["unit_id"]).nunique()
        self.assertTrue((unique_effects == 1).all())


class RunExpCRidTests(unittest.TestCase):
    def test_prepare_precommitment_normalizes_and_truncates(self):
        scenario = {
            "scenario_id": "s01",
            "title": "Test Scenario",
            "research_question": "Did treatment increase outcomes?",
        }
        raw_text = json.dumps({
            "identification_strategy": "Difference-in-differences with treated and control firms",
            "method_family": "DiD",
            "directional_hypothesis": "positive",
            "specifications": [
                {"name": f"spec_{idx}", "description": f"specification {idx}"}
                for idx in range(1, 7)
            ],
            "falsification_gate": "Reject if the estimate turns negative or fails parallel trends.",
        })

        precommitment = prepare_precommitment(raw_text, scenario, "gpt-4o")

        self.assertEqual(precommitment["method_family"], "DID")
        self.assertEqual(precommitment["directional_hypothesis"], "positive")
        self.assertEqual(len(precommitment["allowed_specifications"]), 5)
        self.assertTrue(precommitment["metadata"]["specifications_truncated"])


if __name__ == "__main__":
    unittest.main()
