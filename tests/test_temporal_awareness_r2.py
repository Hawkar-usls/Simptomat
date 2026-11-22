"""R2 tests: exhaustively check 5-trial synthetic pattern overclaim guards."""
import unittest

from tools.temporal_awareness_r2 import (
    N_SYNTHETIC_VECTORS, SCIENTIFIC_GATE, ambiguity_demo, audit,
    score_vector, wilson_interval,
)


class TemporalIdentifiabilityR2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit()

    def test_all_possible_task_count_combinations(self):
        r = self.report
        self.assertEqual(r["R1_total_vectors"], 6**4)
        self.assertEqual(sum(r["profiles_by_R1_descriptive_verdict"].values()), N_SYNTHETIC_VECTORS)

    def test_admissible_synthetic_counts_are_never_rejected(self):
        self.assertEqual(self.report["invalid_synthetic_vectors"], 0)

    def test_science_claim_ceiling_never_broken(self):
        self.assertEqual(self.report["scientific_guard_violations"], 0)
        self.assertFalse(self.report["clinical_validation"])
        self.assertFalse(self.report["patient_data_used"])
        self.assertFalse(self.report["timeless_consciousness_proven"])
        self.assertFalse(self.report["physical_time_travel_proven"])

    def test_no_production_changes(self):
        self.assertFalse(self.report["live_simptomat_interface_modified"])
        self.assertFalse(self.report["production_model_weights_updated"])

    def test_single_score_flip_sometimes_changes_classification(self):
        r = self.report
        self.assertGreater(r["neighbor_label_flips_directed"], 0)
        self.assertLess(r["neighbor_label_flips_directed"], r["neighbors_comparisons_directed"])
        self.assertGreater(r["one_point_unstable_vectors"], 0)
        self.assertEqual(r["one_point_unstable_vectors"] + r["one_point_stable_vectors"], 1296)

    def test_fraction_matches_counts(self):
        r = self.report
        self.assertAlmostEqual(r["neighbor_flip_fraction"],
                               r["neighbor_label_flips_directed"]/r["neighbors_comparisons_directed"],
                               places=6)

    def test_sequence_and_retrieval_are_distinct_descriptive_patterns(self):
        a = score_vector((5,5,1,5))
        b = score_vector((5,5,5,1))
        self.assertEqual(a["verdict"], "SEQUENCE_SPECIFIC_DISSOCIATION_CANDIDATE")
        self.assertEqual(b["verdict"], "DELAYED_RECALL_SPECIFIC_DISSOCIATION_CANDIDATE")
        self.assertNotEqual(a["verdict"], b["verdict"])

    def test_alternative_latent_causes_identical_observation(self):
        r = ambiguity_demo()
        self.assertTrue(r["same_observables_under_competing_causes"])
        self.assertFalse(r["causal_mechanism_identifiable_from_four_counts"])
        self.assertEqual(len(r["possible_competing_causes"]), 2)

    def test_subjective_timelessness_claim_must_never_follow(self):
        for counts in ((5,5,1,5), (5,5,5,1), (5,5,1,1), (0,0,0,0), (5,5,5,5)):
            x = score_vector(counts, felt_no_time_flow=True)
            self.assertFalse(x["timeless_consciousness_proven"])
            self.assertFalse(x["physical_time_travel_proven"])
            self.assertEqual(x["alzheimer_status"], "NOT_EVALUATED")

    def test_wilson_ranges_overlap_at_five_trials(self):
        lo1, hi1 = wilson_interval(1)
        lo4, hi4 = wilson_interval(4)
        self.assertLess(lo4, hi1)
        self.assertTrue(self.report["demonstrative_five_trial_uncertainty"]["intervals_overlap"])

    def test_published_p_is_a_non_significant_negative_control(self):
        study = self.report["literature_sanity"]
        self.assertEqual(study["article_doi"], "10.12779/dnd.2023.22.4.148")
        self.assertEqual(study["reported_temporal_window_group_p"], 0.15)
        self.assertFalse(study["statistically_significant_at_p_below_0_05"])

    def test_no_raw_external_dataset_claim(self):
        self.assertEqual(self.report["scientific_gate"], SCIENTIFIC_GATE)
        self.assertEqual(self.report["literature_sanity"]["additional_paper_data_availability"],
                         "ON_REASONABLE_REQUEST_NOT_OBTAINED")

    def test_bad_counts_fail_closed(self):
        for bad in ((-1,5,5,5), (5,5,5,6), (True,5,5,5), (1,2,3), [1,2,3,4]):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    score_vector(bad)

    def test_bad_uncertainty_argument_fails(self):
        for args in [(-1,5), (6,5), (1,0), (True,5), (1,True)]:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    wilson_interval(*args)

    def test_all_dimensional_classes_present(self):
        classes = self.report["profiles_by_R1_descriptive_verdict"]
        self.assertIn("SEQUENCE_SPECIFIC_DISSOCIATION_CANDIDATE", classes)
        self.assertIn("DELAYED_RECALL_SPECIFIC_DISSOCIATION_CANDIDATE", classes)
        self.assertIn("MIXED_SEQUENCE_AND_DELAYED_RECALL_DISSOCIATION_CANDIDATE", classes)
        self.assertIn("INDETERMINATE_ONLINE_ENGAGEMENT_CONFOUND", classes)
        self.assertIn("INDETERMINATE_IMMEDIATE_ENCODING_CONFOUND", classes)

    def test_report_is_aggregate_not_individual_cases(self):
        r = self.report
        self.assertNotIn("subjects", r)
        self.assertNotIn("patients", r)
        self.assertNotIn("participant_ids", r)
        self.assertEqual(r["source"], "COMPLETE_ENUMERATION_0_TO_5__NO_HUMAN_DATA")


if __name__ == "__main__":
    unittest.main()
