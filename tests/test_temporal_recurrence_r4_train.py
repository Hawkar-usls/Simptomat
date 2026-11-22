"""R4 synthetic learning, chronology and clinical/physics safety contracts."""
import unittest
from datetime import datetime, timezone

from tools.temporal_recurrence_r4_train import (
    CLASSES, FEATURE_NAMES, generate_case, features,
    relative_day, train_and_evaluate,
)


class R4TemporalRecurrenceTrainingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = train_and_evaluate()

    def test_real_parameter_training_occurred(self):
        r = self.receipt
        self.assertEqual(r["model"], "MULTICLASS_LINEAR_SOFTMAX_SGD_STDLIB")
        self.assertEqual(r["model_parameters_trained"], len(CLASSES)*len(FEATURE_NAMES))
        self.assertTrue(any(abs(w) > 0.001 for row in r["weights"] for w in row))

    def test_independent_holdout_family_split(self):
        r = self.receipt
        self.assertFalse(r["family_overlap"])
        self.assertEqual((r["train_cases"],r["validation_cases"],r["heldout_test_cases"]),
                         (3360,560,980))

    def test_baseline_and_model_evaluation(self):
        r = self.receipt
        self.assertGreaterEqual(r["heldout_accuracy"], 0.90)
        self.assertGreater(r["heldout_accuracy"], r["constant_majority_baseline_accuracy"])
        self.assertTrue(r["training_qualified_synthetic"])

    def test_deterministic_receipts(self):
        self.assertEqual(train_and_evaluate(), self.receipt)

    def test_no_patient_data_or_consciousness_certification(self):
        r = self.receipt
        for flag in ("clinical_training", "patient_data_used", "brain_state_inference",
                     "phenomenal_time_measured", "physically_timeless_consciousness_verified",
                     "physical_time_change_verified"):
            self.assertIs(r[flag], False)
        self.assertIn("HOLD", r["scientific_gate"])

    def test_cannot_promote_future_plan_to_observed(self):
        self.assertEqual(self.receipt["prospective_to_observed_misclassifications"], 0)
        for seed in range(5):
            item = generate_case(seed, "FUTURE_PLAN")
            self.assertEqual(item["b_status"], "PLANNED")
            self.assertGreater(item["event_b_time"], item["reference_time"])

    def test_equal_content_can_be_different_event(self):
        item = generate_case(5, "OBSERVED_REPEAT")
        self.assertEqual(item["content_a"], item["content_b"])
        self.assertNotEqual(item["event_a_id"], item["event_b_id"])

    def test_same_event_retains_id(self):
        item = generate_case(5, "SAME_EVENT")
        self.assertEqual(item["event_a_id"], item["event_b_id"])

    def test_recalled_episode_not_new_physical_event(self):
        item = generate_case(5, "MEMORY_OF_EVENT")
        self.assertEqual(item["b_status"], "MEMORY_REFERENCE")
        self.assertEqual(item["event_a_id"], item["event_b_id"])

    def test_continuation_is_not_new_repetition(self):
        item = generate_case(5, "CONTINUING_EVENT")
        self.assertEqual(item["event_a_id"], item["event_b_id"])
        self.assertEqual(item["b_status"], "CONTINUATION")
        self.assertGreater(item["event_b_time"], item["event_a_time"])

    def test_missing_observer_ids_must_stay_ambiguous(self):
        item = generate_case(5, "AMBIGUOUS_REFERENCE")
        self.assertIsNone(item["event_a_id"])
        self.assertIsNone(item["event_b_id"])
        self.assertEqual(item["b_status"], "UNCERTAIN")

    def test_local_yesterday_today_tomorrow_after_date_change(self):
        ref = datetime(2026,11,22,12,tzinfo=timezone.utc)
        for day, answer in [(21,"PAST_1"),(22,"TODAY"),(23,"FUTURE_1"),(24,"FUTURE_2")]:
            event = datetime(2026,11,day,12,tzinfo=timezone.utc)
            self.assertEqual(relative_day(event,ref),answer)

    def test_same_physical_event_gets_new_label_after_a_day(self):
        event = datetime(2026,11,22,12,tzinfo=timezone.utc)
        now = datetime(2026,11,22,14,tzinfo=timezone.utc)
        tomorrow = datetime(2026,11,23,14,tzinfo=timezone.utc)
        self.assertEqual(relative_day(event,now),"TODAY")
        self.assertEqual(relative_day(event,tomorrow),"PAST_1")

    def test_utc_day_not_automatically_local_day(self):
        event = datetime(2026,11,22,23,30,tzinfo=timezone.utc)
        ref = datetime(2026,11,23,0,30,tzinfo=timezone.utc)
        self.assertEqual(relative_day(event,ref,"Europe/Kyiv"),"TODAY")
        self.assertEqual(relative_day(event,ref,"UTC"),"PAST_1")

    def test_dst_local_labels_have_no_invented_elapsed_time(self):
        ref = datetime(2026,3,28,23,30,tzinfo=timezone.utc)
        event = datetime(2026,3,29,1,30,tzinfo=timezone.utc)
        self.assertEqual(relative_day(event,ref,"Europe/Kyiv"),"TODAY")
        self.assertEqual((event-ref).total_seconds(),7200)

    def test_naive_times_rejected(self):
        event = datetime(2026,11,22,12)
        ref = datetime(2026,11,22,14,tzinfo=timezone.utc)
        with self.assertRaises(ValueError):
            relative_day(event,ref)

    def test_invalid_training_input_rejected(self):
        with self.assertRaises(ValueError):
            generate_case(-1,"SAME_EVENT")
        with self.assertRaises(ValueError):
            generate_case(0,"CLINICAL_DIAGNOSIS")

    def test_unsynthetic_input_rejected(self):
        item=generate_case(3,"OBSERVED_REPEAT")
        item["synthetic_only"]=False
        with self.assertRaises(ValueError):
            features(item)

    def test_heldout_confusion_sums_to_all_test_examples(self):
        r=self.receipt
        self.assertEqual(sum(sum(row.values()) for row in r["heldout_confusion"].values()),
                         r["heldout_test_cases"])


if __name__=="__main__":
    unittest.main()
