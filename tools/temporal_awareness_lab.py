"""Simptomat × TACHYON: synthetic-only temporal-awareness dissociation audit.

Research instrumentation only. It cannot assess a patient's Alzheimer's status,
test consciousness directly, or infer "timelessness" / real time travel.
All accepted examples are explicitly synthetic. No live medical input, network,
model weights, user tracking, or physical stimulation is supported.
"""
from __future__ import annotations

import argparse
import json
import math
from collections.abc import Mapping

SCHEMA = "simptomat.tachyon.temporal_awareness.synthetic.v1"
TRIAL_KEYS = ("online_engagement", "immediate_recognition",
              "temporal_order", "delayed_recall")
FORBIDDEN_KEYS = frozenset({
    "name", "full_name", "email", "phone", "address", "date_of_birth",
    "birth_date", "patient_id", "medical_record_number", "diagnosis",
    "diagnostic_label", "person_id", "private_key", "raw_transcript",
    "video", "audio_recording", "neural_recording", "brain_scan"
})
ALLOWED_SYNTHETIC_TAG = "JANUS_SYNTHETIC_FIXTURE_NO_HUMAN_PARTICIPANTS"

def _result(verdict: str, *, reason: str | None = None, **extra: object) -> dict:
    return {
        "research_only": True,
        "clinical_diagnosis": "NOT_EVALUATED",
        "alzheimer_status": "NOT_EVALUATED",
        "consciousness_status": "NOT_ESTABLISHED",
        "timeless_consciousness_proven": False,
        "physical_time_travel_proven": False,
        "physical_time": "INDEPENDENT_FROM_SUBJECTIVE_REPORT",
        "verdict": verdict,
        "reason": reason,
        **extra,
    }

def _all_keys(value: object):
    if isinstance(value, Mapping):
        for k, v in value.items():
            yield str(k).lower()
            yield from _all_keys(v)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from _all_keys(child)

def _quality(value: object) -> str:
    """Demo-only categories, deliberately *not* clinical norms."""
    if value >= 4:
        return "HIGH_DEMO"
    if value <= 1:
        return "LOW_DEMO"
    return "UNRESOLVED_DEMO"

def evaluate_fixture(record: Mapping) -> dict:
    """Separate immediate engagement, temporal ordering and delayed memory.

    The function only accepts declared synthetic fixtures. For any medical or
    individual human data it is not an authorized assessment tool.
    """
    if not isinstance(record, Mapping):
        return _result("REJECT_INVALID_INPUT", reason="RECORD_NOT_MAPPING")
    if (record.get("schema") != SCHEMA
            or record.get("record_kind") != "SYNTHETIC_ONLY"
            or record.get("source_tag") != ALLOWED_SYNTHETIC_TAG):
        return _result("REJECT_NON_SYNTHETIC", reason="NO_HUMAN_DATA_IN_R1")
    if FORBIDDEN_KEYS.intersection(_all_keys(record)):
        return _result("REJECT_PRIVACY_OR_DIAGNOSIS_FIELDS",
                       reason="IDENTIFIER_OR_CLINICAL_DIAGNOSIS_FIELD")
    start, end = record.get("clock_start_ns"), record.get("clock_end_ns")
    if type(start) is not int or type(end) is not int or end <= start:
        return _result("REJECT_INVALID_INPUT", reason="BAD_EXTERNAL_CLOCK")
    elapsed_s = (end - start) / 1e9
    if not math.isfinite(elapsed_s) or elapsed_s <= 0:
        return _result("REJECT_INVALID_INPUT", reason="BAD_ELAPSED_TIME")
    data = record.get("tasks")
    if not isinstance(data, Mapping) or set(data) != set(TRIAL_KEYS):
        return _result("REJECT_INVALID_INPUT", reason="MISSING_OR_UNKNOWN_TASK")
    counts = {}
    for key in TRIAL_KEYS:
        item = data[key]
        if (not isinstance(item, Mapping) or set(item) != {"correct", "total"}
                or type(item["correct"]) is not int or type(item["total"]) is not int
                or item["total"] != 5 or not 0 <= item["correct"] <= 5):
            return _result("REJECT_INVALID_INPUT", reason="INVALID_SYNTHETIC_TASK_COUNTS")
        counts[key] = item["correct"]

    # A subjective report can neither certify consciousness nor prove
    # changed physical clocks. Do not treat absence of it as normality.
    report = record.get("felt_no_time_flow")
    if report is not None and type(report) is not bool:
        return _result("REJECT_INVALID_INPUT", reason="INVALID_FIRST_PERSON_REPORT")

    quality = {k: _quality(v) for k, v in counts.items()}
    on, rec, seq, delayed = (quality[k] for k in TRIAL_KEYS)
    if on != "HIGH_DEMO":
        verdict = "INDETERMINATE_ONLINE_ENGAGEMENT_CONFOUND"
    elif rec != "HIGH_DEMO":
        verdict = "INDETERMINATE_IMMEDIATE_ENCODING_CONFOUND"
    elif seq == "LOW_DEMO" and delayed == "HIGH_DEMO":
        verdict = "SEQUENCE_SPECIFIC_DISSOCIATION_CANDIDATE"
    elif seq == "HIGH_DEMO" and delayed == "LOW_DEMO":
        verdict = "DELAYED_RECALL_SPECIFIC_DISSOCIATION_CANDIDATE"
    elif seq == "LOW_DEMO" and delayed == "LOW_DEMO":
        verdict = "MIXED_SEQUENCE_AND_DELAYED_RECALL_DISSOCIATION_CANDIDATE"
    elif seq == "HIGH_DEMO" and delayed == "HIGH_DEMO":
        verdict = "NO_DEMO_DISSOCIATION"
    else:
        verdict = "INDETERMINATE_MIXED_OR_MIDRANGE"

    return _result(
        verdict,
        reason="DEMO_PROFILE_NOT_CLINICAL_DIAGNOSIS",
        objective_elapsed_s=elapsed_s,
        dimensions=quality,
        task_counts=counts,
        first_person_no_time_flow_report=("REPORTED" if report is True
                                          else "NOT_REPORTED" if report is False
                                          else "NOT_COLLECTED"),
        subjective_timelessness_inference="NOT_ESTABLISHED",
        data_origin="SYNTHETIC_ONLY",
        thresholds="DEMO_5_TRIAL_HIGH_GE4_LOW_LE1_NOT_CLINICAL",
        next_scientific_step="INDEPENDENT_PREREGISTERED_ETHICALLY_APPROVED_STUDY",
    )

def synthetic_case(profile: str, *, felt_no_time_flow: bool | None = None) -> dict:
    """Build named, clearly non-human toy cases to challenge the evidence gate."""
    examples = {
        "ORDER_ONLY": [5, 5, 1, 5],
        "RECALL_ONLY": [5, 5, 5, 1],
        "ENCODING_CONFOUND": [5, 1, 1, 1],
        "LOW_ENGAGEMENT": [1, 1, 1, 1],
        "MIXED": [5, 5, 1, 1],
        "NO_DISSOCIATION": [5, 5, 5, 5],
        "AMBIGUOUS": [5, 5, 3, 3],
    }
    if profile not in examples:
        raise ValueError("Unknown synthetic profile")
    return {
        "schema": SCHEMA,
        "record_kind": "SYNTHETIC_ONLY",
        "source_tag": ALLOWED_SYNTHETIC_TAG,
        "clock_start_ns": 1_000_000_000,
        "clock_end_ns": 301_000_000_000,
        "tasks": {k: {"correct": v, "total": 5}
                  for k, v in zip(TRIAL_KEYS, examples[profile])},
        "felt_no_time_flow": felt_no_time_flow,
    }

def demo() -> dict:
    results = {
        profile: evaluate_fixture(synthetic_case(profile, felt_no_time_flow=True))
        for profile in ("ORDER_ONLY", "RECALL_ONLY", "ENCODING_CONFOUND",
                        "LOW_ENGAGEMENT", "MIXED", "NO_DISSOCIATION", "AMBIGUOUS")
    }
    return {
        "schema": "simptomat.tachyon.temporal_awareness.offline_demo_receipt.v1",
        "run_type": "SYNTHETIC_ONLY",
        "scientific_gate": "HOLD_NO_HUMAN_VALIDATION",
        "clinical_authority": False,
        "patient_data_used": False,
        "independent_real_world_replication": False,
        "rule001": "JANUS_USER_DESIGNATED_RESEARCH_HYPOTHESIS",
        "profiles": results,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic-only Simptomat×TACHYON temporal awareness R1")
    parser.add_argument("--demo", action="store_true", help="run seven synthetic-only profiles")
    args = parser.parse_args()
    if not args.demo:
        parser.error("only --demo is supported; human medical input is prohibited")
    print(json.dumps(demo(), ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
