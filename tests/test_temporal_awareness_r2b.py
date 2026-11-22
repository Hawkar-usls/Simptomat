"""R2B checks use analytic grid counts and full-distribution witnesses."""
from collections import Counter
from fractions import Fraction
import itertools
import json
import unittest

from tools.temporal_awareness_r2 import score_vector
from tools.temporal_awareness_r2b import (
    CANDIDATES, EDGES, GRID, SEEDS, audit, boundary_metrics,
    forward_probabilities, observation_mass, threshold_verdict,
)


class IndependentMethodsR2B(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_exact_historical_reproduction_and_arithmetic(self):
        r = self.result["r1_reproduction"]
        self.assertEqual(r["grid_vectors"], 1296)
        self.assertEqual(r["directed_neighbor_comparisons"], 8640)
        self.assertEqual(r["directed_label_flips"], 704)
        self.assertEqual(r["unstable_vectors"], 532)
        self.assertEqual(r["stable_vectors"], 764)
        self.assertEqual(r["dissociation_candidate_vectors"], 48)
        self.assertEqual(r["indeterminate_vectors"], 1232)
        self.assertEqual(r["no_demo_dissociation_vectors"], 16)
        self.assertEqual(r["noncandidate_vectors"], 1248)
        self.assertEqual(48 + 1232 + 16, r["grid_vectors"])
        self.assertIsNone(r["clinical_prevalence_estimate"])

    def test_sensitivity_base_is_pointwise_identical_to_actual_r1(self):
        for point in GRID:
            self.assertEqual(threshold_verdict(point), score_vector(point)["verdict"])

    def test_grid_edges_have_exact_geometric_count_and_reverse(self):
        # Four axes, five intervals, 6^3 choices of other coordinates, two directions.
        self.assertEqual(len(EDGES), 4 * 5 * 6**3 * 2)
        edge_set = set(EDGES)
        self.assertEqual(len(edge_set), len(EDGES))
        self.assertTrue(all((b, a) in edge_set for a, b in EDGES))
        for a, b in EDGES:
            self.assertEqual(sum(abs(x-y) for x, y in zip(GRID[a], GRID[b])), 1)

    def test_constant_and_one_feature_have_analytic_boundary_counts(self):
        b = self.result["baseline_comparison"]
        self.assertEqual(b["constant"]["directed_label_flips"], 0)
        self.assertEqual(b["constant"]["unstable_vectors"], 0)
        t = b["one_feature_threshold"]
        self.assertEqual(t["directed_label_flips"], 2 * 6**3)
        self.assertEqual(t["unstable_vectors"], 2 * 6**3)
        self.assertEqual(t["flip_fraction"], .05)
        self.assertEqual(t["class_counts"], {"HIGH": 432, "OTHER": 864})

    def test_random_controls_are_frozen_seeded_label_maps(self):
        b = self.result["baseline_comparison"]
        uniform = b["uniform_seven_class_iid"]
        self.assertEqual(uniform["seeds"], list(SEEDS))
        self.assertAlmostEqual(uniform["expected_flip_fraction"], 6/7)
        self.assertGreater(uniform["mean_flip_fraction"], .80)
        self.assertLess(uniform["mean_flip_fraction"], .90)
        for sample in uniform["samples"]:
            self.assertEqual(sample["directed_label_flips"] % 2, 0)
            self.assertEqual(sum(sample["class_counts"].values()), len(GRID))

    def test_permutation_preserves_all_counts_and_uses_without_replacement_expectation(self):
        b = self.result["baseline_comparison"]["r1_histogram_preserving_random_permutation"]
        counts = self.result["r1_reproduction"]["class_counts"]
        expected = 1 - sum(Fraction(n * (n-1), 1296 * 1295) for n in counts.values())
        self.assertAlmostEqual(b["expected_flip_fraction"], float(expected))
        self.assertGreater(b["expected_flip_fraction"], b["iid_same_marginal_comparison_only"])
        for sample in b["samples"]:
            self.assertEqual(sample["class_counts"], counts)
            self.assertEqual(sample["directed_label_flips"] % 2, 0)

    def test_all_threshold_pairs_match_analytic_candidate_count(self):
        sensitivity = self.result["threshold_sensitivity"]
        self.assertEqual(len(sensitivity["rows"]), 15)
        observed_pairs = set()
        for row in sensitivity["rows"]:
            low, high = row["low_at_most"], row["high_at_least"]
            observed_pairs.add((low, high))
            n_low, n_high = low + 1, 6 - high
            # Engagement and recognition HIGH; seq/recall can be LH, HL or LL.
            expected = n_high**2 * (2 * n_low * n_high + n_low**2)
            self.assertEqual(row["candidate_vectors"], expected)
            self.assertEqual(sum(row["class_counts"].values()), 1296)
            m = row["candidate_membership_vs_r1"]
            self.assertEqual(m["retained"] + m["lost"], 48)
            self.assertEqual(m["retained"] + m["new"], expected)
        self.assertEqual(observed_pairs, set(itertools.combinations(range(6), 2)))

    def test_base_threshold_membership_identity_and_changes_elsewhere(self):
        rows = self.result["threshold_sensitivity"]["rows"]
        base = next(r for r in rows if (r["low_at_most"], r["high_at_least"]) == (1, 4))
        self.assertEqual(base["candidate_membership_vs_r1"], {"retained": 48, "lost": 0, "new": 0, "jaccard": 1.0})
        self.assertEqual(base["label_changes_vs_r1"], 0)
        self.assertEqual(base["directed_label_flips"], 704)
        self.assertTrue(any(r["candidate_membership_vs_r1"]["lost"] > 0 for r in rows))
        self.assertTrue(any(r["candidate_membership_vs_r1"]["new"] > 0 for r in rows))

    def test_constructive_witnesses_are_distinct_latents_same_observations(self):
        model = self.result["constructive_nonidentifiability"]
        self.assertGreaterEqual(len(model["witnesses"]), 5)
        for witness in model["witnesses"]:
            self.assertNotEqual(witness["latent_A"], witness["latent_B"])
            self.assertTrue(witness["same_forward_probabilities"])
            self.assertTrue(witness["positive_identical_observation_probability"])
            self.assertEqual(witness["exact_observation_probability_A"], witness["exact_observation_probability_B"])
        self.assertFalse(model["distinct_observable_vectors_used_as_nonidentifiability_proof"])
        self.assertFalse(model["flip_statistics_used_as_nonidentifiability_proof"])

    def test_entire_joint_distributions_identical_and_normalized(self):
        # Equal full PMFs demonstrate nonidentifiability, rather than the weaker
        # property of two stories sharing one nonzero-likelihood observation.
        for witness in self.result["constructive_nonidentifiability"]["witnesses"]:
            latent_a, latent_b = witness["latent_A"], witness["latent_B"]
            p_a = forward_probabilities(tuple(latent_a["capacity_fifths"]),
                                        tuple(latent_a["task_access_fifths"]))
            p_b = forward_probabilities(tuple(latent_b["capacity_fifths"]),
                                        tuple(latent_b["task_access_fifths"]))
            masses_a = [observation_mass(y, p_a) for y in GRID]
            masses_b = [observation_mass(y, p_b) for y in GRID]
            self.assertEqual(masses_a, masses_b)
            self.assertEqual(sum(masses_a), Fraction(1))

    def test_forward_map_depends_on_both_factors(self):
        self.assertEqual(forward_probabilities((5,5,2,5), (5,5,5,5))[2], Fraction(2,5))
        self.assertEqual(forward_probabilities((5,5,2,5), (5,5,1,5))[2], Fraction(2,25))
        self.assertNotEqual(forward_probabilities((5,5,2,5), (5,5,5,5)),
                            forward_probabilities((5,5,2,5), (5,5,1,5)))

    def test_invalid_synthetic_parameters_rejected(self):
        for bad in ((-1,1,1,1), (6,1,1,1), (True,1,1,1), (1,2,3), [1,2,3,4]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                threshold_verdict(bad)
        for low, high in ((1,1), (4,1), (-1,4), (0,6), (False,4), (1,True)):
            with self.subTest(low=low, high=high), self.assertRaises(ValueError):
                threshold_verdict((5,5,1,5), low, high)
        with self.assertRaises(ValueError):
            boundary_metrics(["X"])
        with self.assertRaises(ValueError):
            observation_mass((5,5,1,5), (Fraction(-1),) * 4)

    def test_report_is_deterministic_and_json_serializable(self):
        self.assertEqual(json.dumps(self.result, sort_keys=True), json.dumps(audit(), sort_keys=True))

    def test_scientific_and_runtime_ceiling_remains_hold(self):
        r = self.result
        self.assertEqual(r["scientific_gate"], "HOLD_NO_INDEPENDENT_PARTICIPANT_LEVEL_VALIDATION")
        self.assertTrue(r["R1_classifier_unchanged"])
        for key in ("human_data_analyzed", "patient_data_ingested", "independent_clinical_replication",
                    "clinical_validation", "live_screening_enabled", "production_model_weights_changed",
                    "timeless_consciousness_proven", "physical_time_travel_proven"):
            self.assertIs(r[key], False)
        self.assertEqual(r["baseline_comparison"]["oracle_ceiling"], "NOT_DEFINED_NO_INDEPENDENT_GROUND_TRUTH")


if __name__ == "__main__":
    unittest.main()
