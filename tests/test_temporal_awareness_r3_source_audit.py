"""R3 source-scoping tests, no human data loaded or contacted."""
import copy
import json
import unittest
from pathlib import Path

from tools.temporal_awareness_r3_source_audit import (
    REQUIRED_AXES, SCIENTIFIC_HOLD, _fail, audit_manifest, evaluate_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research/temporal_awareness/SIMPTOMAT_TACHYON_R3_INDEPENDENT_DATA_SCOUT_2026-11-22.json"


def doc():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


class R3IndependentDataQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = doc()
        cls.report = audit_manifest(cls.manifest)

    def test_r3_scientific_hold_not_hidden(self):
        self.assertEqual(self.report["scientific_gate"], SCIENTIFIC_HOLD)
        self.assertEqual(self.report["datasets_qualified"], 0)
        self.assertEqual(self.report["individual_level_models_tested"], 0)

    def test_sources_identified_no_patient_records(self):
        self.assertEqual(self.report["sources_audited"], 6)
        self.assertEqual(self.report["real_participant_records_seen"], 0)
        self.assertFalse(self.report["participant_level_evidence_available_to_janus"])

    def test_explicit_axes_are_distinct(self):
        self.assertEqual(tuple(x["key"] for x in self.manifest["required_axes"]), REQUIRED_AXES)

    def test_no_source_qualifies_with_published_metadata(self):
        for item in self.report["candidates"]:
            self.assertFalse(item["dataset_ready_for_independent_empirical_test"])
            self.assertFalse(item["participant_rows_read"])

    def test_all_citations_have_nonempty_links(self):
        for item in self.manifest["candidates"]:
            self.assertTrue(item["url"].startswith("https://"))
            self.assertTrue(item["id"])

    def test_2023_teghil_not_yet_four_direct(self):
        a = next(x for x in self.report["candidates"] if x["source_id"]=="TEGHIL_2023")
        self.assertIn("temporal_order", a["required_axes_not_yet_directly_verified"])
        self.assertIn("online_engagement", a["required_axes_not_yet_directly_verified"])

    def test_no_inference_from_calendar_order_of_lessons(self):
        a = next(x for x in self.report["candidates"] if x["source_id"]=="SEATTLE_GRONINGEN_2026")
        self.assertIn("temporal_order", a["required_axes_not_yet_directly_verified"])

    def test_zenodo_restricted_not_open(self):
        a = next(x for x in self.report["candidates"] if x["source_id"]=="ZENODO_COG_CONNECTOME_2026")
        self.assertIn("RESTRICTED", a["source_data_access_status"])
        self.assertFalse(a["authorization_metadata_asserted"])

    def test_open_osf_url_is_not_file_access(self):
        for s in ("PAYNE_2023", "SEATTLE_GRONINGEN_2026"):
            a = next(x for x in self.report["candidates"] if x["source_id"] == s)
            self.assertFalse(a["dataset_ready_for_independent_empirical_test"])
            self.assertFalse(a["participant_rows_read"])

    def test_on_request_data_not_treated_as_received(self):
        self.assertEqual(self.manifest["requested_but_not_sent"]["no_email_sent"], True)
        self.assertEqual(self.manifest["requested_but_not_sent"]["no_files_received"], True)

    def test_not_medical_diagnostic_or_time_machine(self):
        self.assertFalse(self.report["clinical_authority"])
        self.assertFalse(self.report["physical_timelessness_proven"])
        self.assertFalse(self.report["time_travel_proven"])
        self.assertTrue(self.report["no_automated_email_sent"])

    def test_unknown_axis_cannot_silently_pass(self):
        a = copy.deepcopy(self.manifest["candidates"][0])
        a["axes"]["temporal_order"]["coverage"] = "MAYBE_SOME_DATA"
        self.assertEqual(evaluate_candidate(a)["reason"], "INVALID_COVERAGE_LABEL")

    def test_missing_axis_rejected(self):
        a = copy.deepcopy(self.manifest["candidates"][0])
        del a["axes"]["online_engagement"]
        self.assertEqual(evaluate_candidate(a)["reason"], "MISSING_OR_EXTRA_AXES")

    def test_missing_access_flags_rejected(self):
        a = copy.deepcopy(self.manifest["candidates"][0])
        del a["rights_verified"]
        self.assertEqual(evaluate_candidate(a)["reason"], "MISSING_ACCESS_VERIFICATION_FLAGS")

    def test_maliciously_faked_all_direct_still_requires_private_audit(self):
        a = copy.deepcopy(self.manifest["candidates"][0])
        for k in REQUIRED_AXES:
            a["axes"][k]["coverage"] = "DIRECT_BUT_FILES_NOT_INSPECTED"
        for k in ("rights_verified", "participant_rows_available_to_janus", "source_data_access_verified"):
            a[k] = True
        v = evaluate_candidate(a)
        self.assertEqual(v["status"], "HOLD_INDEPENDENT_PRIVATE_FILE_AUDIT")
        self.assertFalse(v["dataset_ready_for_independent_empirical_test"])

    def test_any_claim_real_data_ingested_fails(self):
        p = copy.deepcopy(self.manifest)
        p["real_participant_data_imported"] = True
        self.assertEqual(audit_manifest(p)["reason"], "IMPROPER_HUMAN_DATA_CLAIM")

    def test_schema_override_denied(self):
        p = copy.deepcopy(self.manifest)
        p["schema"] = "simptomat.tachyon.r3.clinical_auto_diagnosis"
        self.assertEqual(audit_manifest(p)["reason"], "BAD_R3_SCHEMA")

    def test_duplicate_sources_denied(self):
        p = copy.deepcopy(self.manifest)
        p["candidates"].append(copy.deepcopy(p["candidates"][0]))
        self.assertEqual(audit_manifest(p)["reason"], "DUPLICATE_SOURCE_ID")

    def test_empty_source_list_denied(self):
        p = copy.deepcopy(self.manifest)
        p["candidates"] = []
        self.assertEqual(audit_manifest(p)["reason"], "NO_SOURCE_CANDIDATES")

    def test_indirect_proxies_are_not_direct(self):
        self.assertGreater(sum(self.report["unknown_or_not_direct_counts"].values()), 0)
        for key in REQUIRED_AXES:
            self.assertGreater(self.report["unknown_or_not_direct_counts"][key], 0)


if __name__ == "__main__":
    unittest.main()
