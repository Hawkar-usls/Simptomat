"""Simptomat TACHYON R1: purely synthetic, nonclinical adversarial evidence tests."""
from __future__ import annotations
import copy
import unittest

from tools.temporal_awareness_lab import (
    SCHEMA, evaluate_fixture, synthetic_case, demo,
)


class TemporalAwarenessResearchTests(unittest.TestCase):
    def test_order_weak_recall_preserved_separate(self):
        r = evaluate_fixture(synthetic_case("ORDER_ONLY", felt_no_time_flow=True))
        self.assertEqual(r["verdict"], "SEQUENCE_SPECIFIC_DISSOCIATION_CANDIDATE")
        self.assertEqual(r["dimensions"]["delayed_recall"], "HIGH_DEMO")
        self.assertEqual(r["first_person_no_time_flow_report"], "REPORTED")
        self.assertFalse(r["timeless_consciousness_proven"])

    def test_delayed_memory_weak_order_preserved_separate(self):
        r = evaluate_fixture(synthetic_case("RECALL_ONLY", felt_no_time_flow=True))
        self.assertEqual(r["verdict"], "DELAYED_RECALL_SPECIFIC_DISSOCIATION_CANDIDATE")
        self.assertEqual(r["dimensions"]["temporal_order"], "HIGH_DEMO")

    def test_encoding_confound_does_not_claim_order_problem(self):
        r = evaluate_fixture(synthetic_case("ENCODING_CONFOUND"))
        self.assertEqual(r["verdict"], "INDETERMINATE_IMMEDIATE_ENCODING_CONFOUND")

    def test_poor_online_checks_no_consciousness_inference(self):
        r = evaluate_fixture(synthetic_case("LOW_ENGAGEMENT", felt_no_time_flow=True))
        self.assertEqual(r["verdict"], "INDETERMINATE_ONLINE_ENGAGEMENT_CONFOUND")
        self.assertEqual(r["consciousness_status"], "NOT_ESTABLISHED")

    def test_both_difficulties_preserve_mixed_not_single(self):
        r = evaluate_fixture(synthetic_case("MIXED"))
        self.assertIn("MIXED_SEQUENCE_AND_DELAYED_RECALL", r["verdict"])

    def test_intact_demo_not_alzheimer_negative(self):
        r = evaluate_fixture(synthetic_case("NO_DISSOCIATION"))
        self.assertEqual(r["verdict"], "NO_DEMO_DISSOCIATION")
        self.assertEqual(r["alzheimer_status"], "NOT_EVALUATED")

    def test_middling_data_abstains(self):
        self.assertEqual(evaluate_fixture(synthetic_case("AMBIGUOUS"))["verdict"],
                         "INDETERMINATE_MIXED_OR_MIDRANGE")

    def test_absent_report_is_uncollected_not_no_timelessness(self):
        r = evaluate_fixture(synthetic_case("ORDER_ONLY"))
        self.assertEqual(r["first_person_no_time_flow_report"], "NOT_COLLECTED")
        self.assertFalse(r["timeless_consciousness_proven"])

    def test_unsupported_real_person_record_rejected(self):
        x = synthetic_case("ORDER_ONLY")
        x["record_kind"] = "CONSENTED_PATIENT"
        self.assertEqual(evaluate_fixture(x)["verdict"], "REJECT_NON_SYNTHETIC")

    def test_patient_diagnosis_field_rejected_even_in_synthetic(self):
        x = synthetic_case("RECALL_ONLY")
        x["diagnosis"] = "ALZHEIMER"
        self.assertEqual(evaluate_fixture(x)["verdict"],
                         "REJECT_PRIVACY_OR_DIAGNOSIS_FIELDS")

    def test_nested_personal_identifier_rejected(self):
        x = synthetic_case("ORDER_ONLY")
        x["metadata"] = {"nested": [{"email": "person@example.com"}]}
        self.assertEqual(evaluate_fixture(x)["verdict"],
                         "REJECT_PRIVACY_OR_DIAGNOSIS_FIELDS")

    def test_no_fake_consent_cannot_override_no_humans(self):
        x = synthetic_case("ORDER_ONLY")
        x["source_tag"] = "REAL_CONSENTED_COHORT"
        x["consent"] = True
        self.assertEqual(evaluate_fixture(x)["verdict"], "REJECT_NON_SYNTHETIC")

    def test_wrong_schema_rejected(self):
        x = synthetic_case("ORDER_ONLY")
        x["schema"] = "simptomat.clinical.diagnosis"
        self.assertEqual(evaluate_fixture(x)["verdict"], "REJECT_NON_SYNTHETIC")

    def test_bad_clock_rejected(self):
        x = synthetic_case("ORDER_ONLY")
        x["clock_end_ns"] = x["clock_start_ns"]
        self.assertEqual(evaluate_fixture(x)["reason"], "BAD_EXTERNAL_CLOCK")

    def test_bool_is_not_count(self):
        x = synthetic_case("ORDER_ONLY")
        x["tasks"]["temporal_order"]["correct"] = True
        self.assertEqual(evaluate_fixture(x)["reason"], "INVALID_SYNTHETIC_TASK_COUNTS")

    def test_count_outside_trial_bound(self):
        x = synthetic_case("ORDER_ONLY")
        x["tasks"]["delayed_recall"]["correct"] = 6
        self.assertEqual(evaluate_fixture(x)["verdict"], "REJECT_INVALID_INPUT")

    def test_missing_task_rejected(self):
        x = synthetic_case("ORDER_ONLY")
        del x["tasks"]["temporal_order"]
        self.assertEqual(evaluate_fixture(x)["reason"], "MISSING_OR_UNKNOWN_TASK")

    def test_malformed_self_report_rejected(self):
        x = synthetic_case("ORDER_ONLY")
        x["felt_no_time_flow"] = "YES"
        self.assertEqual(evaluate_fixture(x)["reason"], "INVALID_FIRST_PERSON_REPORT")

    def test_all_outputs_no_authority(self):
        receipt = demo()
        self.assertFalse(receipt["clinical_authority"])
        self.assertFalse(receipt["patient_data_used"])
        self.assertFalse(receipt["independent_real_world_replication"])
        self.assertEqual(receipt["scientific_gate"], "HOLD_NO_HUMAN_VALIDATION")
        self.assertEqual(len(receipt["profiles"]), 7)
        for v in receipt["profiles"].values():
            self.assertFalse(v["physical_time_travel_proven"])
            self.assertFalse(v["timeless_consciousness_proven"])
            self.assertEqual(v["clinical_diagnosis"], "NOT_EVALUATED")
            self.assertEqual(v["objective_elapsed_s"], 300.0)

    def test_never_recast_disorientation_as_timelessness(self):
        x = synthetic_case("ENCODING_CONFOUND", felt_no_time_flow=True)
        r = evaluate_fixture(x)
        self.assertEqual(r["subjective_timelessness_inference"], "NOT_ESTABLISHED")
        self.assertNotIn("PROVEN", r["verdict"])

if __name__ == "__main__":
    unittest.main()
