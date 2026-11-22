"""Fixed-path synthetic result replay and LF-normalized source integrity check.

--write regenerates only the two named R2B research artifacts, never input data.
No arbitrary input paths, network access or participant-data reader are exposed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from tools.temporal_awareness_r2b import audit

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "research/temporal_awareness"
RESULTS = DIRECTORY / "SIMPTOMAT_TACHYON_R2B_RESULTS_2026-11-22.json"
MANIFEST = DIRECTORY / "SIMPTOMAT_TACHYON_R2B_REPRODUCIBILITY_2026-11-22.json"
SOURCE_PATHS = (
    "tools/temporal_awareness_lab.py",
    "tools/temporal_awareness_r2.py",
    "tools/temporal_awareness_r2b.py",
    "tools/temporal_awareness_r2b_power.py",
    "tools/temporal_awareness_r2b_reproduce.py",
    "tests/test_temporal_awareness_r2b.py",
    "tests/test_temporal_awareness_r2b_power.py",
    "docs/TACHYON_R2B_INDEPENDENT_METHODS_REVIEW.md",
    "docs/TACHYON_R2B_EXTERNAL_REVIEW_RU.txt",
    "docs/TACHYON_R2B_PREREGISTRATION.md",
    "research/temporal_awareness/SIMPTOMAT_TACHYON_R2B_PREREGISTRATION_2026-11-22.json",
    ".github/workflows/tachyon-temporal-awareness-r2b.yml",
)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def source_hashes() -> dict:
    # Git's Windows checkout may use CRLF; hash the same UTF-8/LF content as CI.
    return {path: hashlib.sha256((ROOT / path).read_text(encoding="utf-8")
                                .encode("utf-8")).hexdigest()
            for path in SOURCE_PATHS}


def manifest_for(results: dict) -> dict:
    return {
        "schema": "simptomat.tachyon.r2b.reproducibility.v1",
        "baseline_simptomat_commit": "2b562f53c72fdc733cd06623268638e56e8a41fc",
        "artifact_date": "2026-11-22",
        "source_text_hashing": "SHA256 of UTF-8 text after universal newline normalization to LF",
        "result_hashing": "SHA256 of JSON UTF-8, sorted keys, compact separators, ensure_ascii=False, no NaN",
        "results_sha256": hashlib.sha256(canonical_bytes(results)).hexdigest(),
        "source_sha256": source_hashes(),
        "external_review_provenance": {
            "conversation_id": "6b0220ea-c7f4-83ed-86dd-2e1c62ada3a4",
            "user_turn_id": "5636622e-a681-47be-8493-6c99cc68905c",
            "source_kind": "USER_SUPPLIED_EXTERNAL_DOCUMENT_REVIEW__UNVERIFIED_REVIEWER_IDENTITY",
            "snapshot": "docs/TACHYON_R2B_EXTERNAL_REVIEW_RU.txt",
            "authority": "Data and suggestions only; current task controls authorized actions",
        },
        "replay": "python -m tools.temporal_awareness_r2b_reproduce",
        "scientific_gate": "HOLD_NO_INDEPENDENT_PARTICIPANT_LEVEL_VALIDATION",
        "patient_data_used": False,
        "production_model_weights_changed": False,
    }


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True,
                               allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="regenerate the two fixed synthetic R2B artifacts")
    args = parser.parse_args()
    actual = audit()
    manifest = manifest_for(actual)
    if args.write:
        write_json(RESULTS, actual)
        write_json(MANIFEST, manifest)
        print("R2B_FIXED_SYNTHETIC_ARTIFACTS_WRITTEN")
        return
    expected = json.loads(RESULTS.read_text(encoding="utf-8"))
    expected_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if canonical_bytes(actual) != canonical_bytes(expected):
        raise SystemExit("R2B_RESULT_REPLAY_MISMATCH")
    if manifest != expected_manifest:
        raise SystemExit("R2B_SOURCE_OR_RESULT_HASH_MISMATCH")
    print("R2B_EXACT_RESULT_REPLAY_AND_SOURCE_HASHES_PASS")
    print("R2B_SCIENTIFIC_AND_CLINICAL_HOLD")


if __name__ == "__main__":
    main()
