"""Numerical and design checks; these are software tests, not hypotheses."""
import json
from pathlib import Path
import unittest

from tools.temporal_awareness_r2b_power import (
    paired_t_power, recruitment_plan, report, required_pairs, t_critical,
)


class PairedPowerTest(unittest.TestCase):
    def test_reference_central_t_quantile(self):
        # Independent validation: scipy 1.18.0 t.ppf(.9875,29), not a runtime dependency.
        self.assertAlmostEqual(t_critical(30), 2.363846073208312, places=11)

    def test_reference_noncentral_t_power(self):
        # scipy.stats.nct.sf(tcrit,df,dz*sqrt(n))+nct.cdf(-tcrit,df,dz*sqrt(n)).
        for n, dz, expected in ((20, .3, .16209685259139675),
                                (34, .5, .7130529409904087),
                                (140, .3, .8990316135943264),
                                (313, .2, .9001998240879776)):
            with self.subTest(n=n, dz=dz):
                self.assertAlmostEqual(paired_t_power(n, dz), expected, places=10)

    def test_quadrature_converges(self):
        for n, dz in ((2, .3), (20, .5), (141, .3), (313, .2)):
            with self.subTest(n=n):
                self.assertAlmostEqual(paired_t_power(n, dz, steps=4096),
                                       paired_t_power(n, dz, steps=8192), places=8)

    def test_null_rejection_probability_is_alpha(self):
        for n in (2, 20, 141, 313):
            self.assertAlmostEqual(paired_t_power(n, 0), .025, places=8)

    def test_two_sided_sign_symmetry(self):
        self.assertEqual(paired_t_power(50, -.3), paired_t_power(50, .3))

    def test_more_pairs_raise_power(self):
        self.assertLess(paired_t_power(50, .3), paired_t_power(100, .3))

    def test_all_sample_sizes_are_minimal_at_boundary(self):
        for scenario in report()["scenarios"]:
            n, dz = scenario["evaluable_holdout_pairs"], scenario["assumed_dz"]
            target = scenario["target_marginal_power"]
            self.assertGreaterEqual(paired_t_power(n, dz), target)
            self.assertLess(paired_t_power(n - 1, dz), target)

    def test_reference_selected_design_and_recruitment(self):
        self.assertEqual(required_pairs(.3, .9), 141)
        plan = recruitment_plan(141)
        self.assertEqual(plan["total_evaluable_participants"], 353)
        self.assertEqual(plan["recruitment_target_expected_retention"], 442)

    def test_attrition_and_holdout_inflation(self):
        base = recruitment_plan(141)["recruitment_target_expected_retention"]
        self.assertGreater(recruitment_plan(141, .3)["recruitment_target_expected_retention"], base)
        self.assertGreater(recruitment_plan(141, attrition=.3)["recruitment_target_expected_retention"], base)

    def test_no_prevalence_or_clinical_promotions(self):
        r = report()
        self.assertFalse(r["synthetic_candidate_grid_fraction_used_as_prevalence"])
        self.assertFalse(r["prevalence_test_against_zero_used"])
        self.assertFalse(r["patient_data_used"])
        self.assertFalse(r["clinical_validation"])
        self.assertFalse(r["multiplicity"]["software_unit_tests_are_statistical_hypotheses"])
        self.assertEqual(r["multiplicity"]["confirmatory_family_size"], 2)

    def test_prospective_protocol_matches_power_design(self):
        path = Path(__file__).resolve().parents[1] / "research/temporal_awareness/SIMPTOMAT_TACHYON_R2B_PREREGISTRATION_2026-11-22.json"
        protocol = json.loads(path.read_text(encoding="utf-8"))
        selected = report()["illustrative_selected_design"]
        self.assertEqual(protocol["status"], "PROSPECTIVE_PLAN_PENDING_EXTERNAL_REGISTRATION")
        self.assertFalse(protocol["external_registration_completed"])
        self.assertEqual(protocol["multiplicity"]["confirmatory_hypotheses"], 2)
        self.assertEqual(protocol["power"]["illustrative_minimum_evaluable_holdout_pairs"],
                         selected["evaluable_holdout_pairs"])
        self.assertEqual(protocol["power"]["illustrative_expected_recruitment_target"],
                         selected["recruitment_target_expected_retention"])
        self.assertFalse(protocol["current_gates_passed_for_real_data"])
        self.assertTrue(all("external_eligible_reference" in item["definition"]
                            for item in protocol["primary_endpoints"]))

    def test_invalid_power_inputs(self):
        for args in ((1, .3), (True, .3), (20, float("nan")), (20, .3, 0),
                     (20, .3, .025, 257)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                paired_t_power(*args)

    def test_invalid_planning_inputs(self):
        for args in ((0,), (-.3,), (.3, 1), (.3, float("nan"))):
            with self.subTest(args=args), self.assertRaises(ValueError):
                required_pairs(*args)
        for args in ((1,), (141, 1), (141, .4, 1), (141, .4, -.1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                recruitment_plan(*args)


if __name__ == "__main__":
    unittest.main()
