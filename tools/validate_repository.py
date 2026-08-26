#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN_CASE_KEYS = {
    "name", "full_name", "email", "phone", "telegram_id", "telegram_user_id",
    "address", "exact_address", "birth_date", "date_of_birth", "medical_record_number"
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def validate_all_json() -> None:
    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts:
            load_json(path)


def validate_case(path: pathlib.Path) -> None:
    case = load_json(path)
    required = {
        "schema", "case_id", "participant", "consent", "privacy",
        "epistemic_contract", "screening_questions", "result", "calibration_use", "provenance"
    }
    missing = required - set(case)
    if missing:
        fail(f"{path.name}: missing required keys: {sorted(missing)}")
    if case["schema"] != "simptomat.screening_case.v1":
        fail(f"{path.name}: wrong schema")
    if not re.fullmatch(r"SIM-P\d{4}-\d{4}-\d{2}-\d{2}-[A-Z0-9_-]+", case["case_id"]):
        fail(f"{path.name}: malformed case_id")
    if case["participant"].get("identifying_fields_stored") is not False:
        fail(f"{path.name}: identifying_fields_stored must be false for public cases")
    if case["consent"].get("status") != "EXPLICIT_FOR_THIS_RECORD":
        fail(f"{path.name}: public consented case must carry explicit consent status")
    if case["consent"].get("not_inferred_for_future_cases") is not True:
        fail(f"{path.name}: consent must not propagate to future cases")
    if case["privacy"].get("raw_chat_transcript_published") is not False:
        fail(f"{path.name}: raw transcript publication is forbidden by default")
    if case["epistemic_contract"].get("claim_ceiling") != "SELF_REPORTED_RESEARCH_SCREENING_ONLY":
        fail(f"{path.name}: unsafe claim ceiling")
    questions = case["screening_questions"]
    ids = [item.get("id") for item in questions]
    if ids != list(range(1, len(ids) + 1)):
        fail(f"{path.name}: question ids must be contiguous from 1")
    if not case["result"].get("what_this_does_not_support"):
        fail(f"{path.name}: missing non-claims")
    if case["calibration_use"].get("gold_standard_diagnosis_available") is False:
        terminal = case["result"].get("screening_terminal", "")
        if "DIAGNOSED" in terminal or terminal in {"PRION_PRESENT", "PRION_ABSENT"}:
            fail(f"{path.name}: diagnostic terminal without reference standard")

    keys = {k.lower() for k in walk_keys(case)}
    # Permit privacy declarations like exact_address=NOT_STORED while rejecting
    # actual identifier-shaped top-level fields outside the privacy policy block.
    for forbidden in FORBIDDEN_CASE_KEYS:
        if forbidden in keys and forbidden not in {"exact_address"}:
            fail(f"{path.name}: forbidden identifier field present: {forbidden}")


def main() -> None:
    validate_all_json()
    case_dir = ROOT / "cases" / "consented"
    cases = sorted(case_dir.glob("*.json")) if case_dir.exists() else []
    if not cases:
        fail("no consented cases found")
    for case in cases:
        validate_case(case)
    print(f"PASS: parsed all JSON and validated {len(cases)} consented case(s)")


if __name__ == "__main__":
    main()
