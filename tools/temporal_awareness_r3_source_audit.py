"""JANUS TACHYON R3: fail-closed independent dataset readiness audit.

Reads only a PUBLIC SOURCES MANIFEST. Does not download, parse, inspect or
score records about people. Does not connect to patients or human experiments.
An author's dataset availability statement is NOT permission, file receipt,
or validated matching of within-subject task measures.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections.abc import Mapping

EXPECTED_SCHEMA = "simptomat.tachyon.r3.independent_data_qualification.v1"
REQUIRED_AXES = ("online_engagement", "immediate_recognition", "temporal_order", "delayed_recall")
DIRECT = "DIRECT_BUT_FILES_NOT_INSPECTED"
PROXY = "INDIRECT_PROXY"
MISSING = "UNKNOWN_OR_NOT_REPORTED"
ALLOWED_LABELS = frozenset((DIRECT, PROXY, MISSING))
DATA_READY_FLAGS = (
    "rights_verified",
    "participant_rows_available_to_janus",
    "source_data_access_verified",
)

SCIENTIFIC_HOLD = "HOLD_NO_QUALIFIED_PARTICIPANT_LEVEL_INDEPENDENT_DATA"


def _fail(reason: str) -> dict:
    return {
        "status": "INVALID_DATASET_MANIFEST",
        "reason": reason,
        "dataset_ready_for_independent_empirical_test": False,
        "real_participant_data_loaded": False,
        "clinical_authority": False,
        "physical_timelessness_proven": False,
    }


def evaluate_candidate(candidate: Mapping) -> dict:
    """Inspect provenance METADATA; never score a person or certify rights."""
    if not isinstance(candidate, Mapping):
        return _fail("CANDIDATE_NOT_MAPPING")
    source_id = candidate.get("id")
    if not isinstance(source_id, str) or not source_id:
        return _fail("MISSING_SOURCE_ID")
    if not candidate.get("url") or not isinstance(candidate.get("url"), str):
        return _fail("MISSING_PUBLICATION")
    axes = candidate.get("axes")
    if not isinstance(axes, Mapping) or set(axes) != set(REQUIRED_AXES):
        return _fail("MISSING_OR_EXTRA_AXES")
    categories = {}
    for key in REQUIRED_AXES:
        item = axes.get(key)
        if not isinstance(item, Mapping):
            return _fail("AXIS_NOT_MAPPING")
        if item.get("coverage") not in ALLOWED_LABELS:
            return _fail("INVALID_COVERAGE_LABEL")
        if not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
            return _fail("AXIS_WITHOUT_EVIDENCE")
        categories[key] = item["coverage"]
    verified_flags = {key: candidate.get(key) for key in DATA_READY_FLAGS}
    if any(type(v) is not bool for v in verified_flags.values()):
        return _fail("MISSING_ACCESS_VERIFICATION_FLAGS")
    # This manifest is intentionally descriptive. A DIRECT label here means
    # the article DESCRIBES the task, not that JANUS actually obtained its rows.
    described_direct = [key for key in REQUIRED_AXES if categories[key] == DIRECT]
    indirect = [key for key in REQUIRED_AXES if categories[key] == PROXY]
    missing = [key for key in REQUIRED_AXES if categories[key] == MISSING]
    missing_evidence = sorted(set(REQUIRED_AXES) - set(described_direct))
    no_data = not all(verified_flags.values())

    # Even full Boolean assertions in a published source register cannot
    # replace an independent private data and consent audit; no ready verdict.
    verdict = (
        "HOLD_UNVERIFIED_PUBLICATION_LEVEL_AXES"
        if missing_evidence
        else "HOLD_INDEPENDENT_PRIVATE_FILE_AUDIT"
    )
    if no_data:
        verdict = "HOLD_SOURCE_ACCESS_AND_TASK_LINKAGE"

    return {
        "source_id": source_id,
        "status": verdict,
        "published_task_descriptions_direct": described_direct,
        "proxies_not_accepted_as_direct": indirect,
        "unreported_required_axes": missing,
        "required_axes_not_yet_directly_verified": missing_evidence,
        "source_data_access_status": candidate.get("data_status"),
        "authorization_metadata_asserted": bool(verified_flags["rights_verified"]),
        "dataset_ready_for_independent_empirical_test": False,
        "participant_rows_read": False,
        "real_participant_data_loaded": False,
        "clinical_authority": False,
        "physical_timelessness_proven": False,
    }


def audit_manifest(doc: Mapping) -> dict:
    if not isinstance(doc, Mapping) or doc.get("schema") != EXPECTED_SCHEMA:
        return _fail("BAD_R3_SCHEMA")
    if doc.get("real_participant_data_imported") is not False:
        return _fail("IMPROPER_HUMAN_DATA_CLAIM")
    if doc.get("clinical_diagnosis_performed") is not False:
        return _fail("IMPROPER_DIAGNOSTIC_CLAIM")
    if doc.get("code_executed_on_real_patient_data") is not False:
        return _fail("IMPROPER_EXECUTION_CLAIM")
    required = doc.get("required_axes")
    if not isinstance(required, list) or [a.get("key") for a in required if isinstance(a, Mapping)] != list(REQUIRED_AXES):
        return _fail("INVALID_REQUIRED_AXIS_CONTRACT")
    candidates = doc.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 1:
        return _fail("NO_SOURCE_CANDIDATES")
    items = [evaluate_candidate(c) for c in candidates]
    if any(item["status"] == "INVALID_DATASET_MANIFEST" for item in items):
        return _fail("SOURCE_RECORD_INVALID")
    ids = [item["source_id"] for item in items]
    if len(ids) != len(set(ids)):
        return _fail("DUPLICATE_SOURCE_ID")
    gaps = {key: sum(item["required_axes_not_yet_directly_verified"].count(key)
                     for item in items) for key in REQUIRED_AXES}
    return {
        "schema": "simptomat.tachyon.r3.source_scoping_receipt.v1",
        "snapshot_date": doc.get("as_of"),
        "scientific_gate": SCIENTIFIC_HOLD,
        "sources_audited": len(items),
        "datasets_qualified": 0,
        "real_participant_records_seen": 0,
        "individual_level_models_tested": 0,
        "participant_level_evidence_available_to_janus": False,
        "source_research_only": True,
        "no_automated_email_sent": True,
        "unknown_or_not_direct_counts": gaps,
        "candidates": items,
        "requirements_for_next_gate": [
            "Authorized privacy-compliant data access + data dictionary + original provenance",
            "Actual same-person four-task matched event chronology and documented delays",
            "Verified file checksums and separation of original study datasets from source descriptions",
            "Predeclared holdout split, clinical expert/ethics review, no diagnostic promotion",
            "No raw human records or identifying data in public GitHub",
        ],
        "clinical_authority": False,
        "physical_timelessness_proven": False,
        "time_travel_proven": False,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="R3 publication-level independent data scout (no patient input)")
    p.add_argument("--audit", action="store_true")
    args = p.parse_args()
    if not args.audit:
        p.error("Only --audit of checked-in publication manifest is supported")
    root = Path(__file__).resolve().parents[1]
    path = root / "research/temporal_awareness/SIMPTOMAT_TACHYON_R3_INDEPENDENT_DATA_SCOUT_2026-11-22.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    result = audit_manifest(doc)
    if result.get("scientific_gate") != SCIENTIFIC_HOLD:
        raise SystemExit("R3 strict gate rejected manifest: " + repr(result))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
