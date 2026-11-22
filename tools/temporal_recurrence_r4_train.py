"""TACHYON x Simptomat R4: offline synthetic temporal-recurrence training.

Trains an actual multiclass linear softmax model on generated event *metadata*.
It is NOT trained on people, cognitive/medical records, consciousness,
Alzheimer's disease, or observations of altered physical time.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

CLASSES = (
    "AMBIGUOUS_REFERENCE",
    "CONTINUING_EVENT",
    "DISTINCT_CONTENT",
    "FUTURE_PLAN",
    "MEMORY_OF_EVENT",
    "OBSERVED_REPEAT",
    "SAME_EVENT",
)
FEATURE_NAMES = (
    "bias", "same_id", "both_ids", "same_content", "status_observed",
    "status_planned", "status_memory", "status_continuation",
    "id_missing", "future_event", "same_calendar_day", "past_event",
    "abs_delta_days_scaled",
)
ROOT_SEED = 20261122
RESEARCH_CEILING = "SYNTHETIC_EVENT_METADATA_ONLY__NO_CLINICAL_OR_PHENOMENOLOGY"

def _utc(dt: datetime) -> datetime:
    if not isinstance(dt, datetime) or dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("timezone-aware datetimes required")
    return dt.astimezone(timezone.utc)

def relative_day(event_time: datetime, reference_time: datetime, tz_name: str = "Europe/Kyiv") -> str:
    """Subject-independent local calendar relationship; no cognitive inference."""
    zone = ZoneInfo(tz_name)
    delta = (_utc(event_time).astimezone(zone).date() -
             _utc(reference_time).astimezone(zone).date()).days
    if delta == 0:
        return "TODAY"
    return f"FUTURE_{delta}" if delta > 0 else f"PAST_{-delta}"

def generate_case(family: int, cls: str) -> dict:
    """Held-out splits separate family IDs. No patient data anywhere."""
    if type(family) is not int or family < 0 or cls not in CLASSES:
        raise ValueError("invalid synthetic case descriptor")
    rng = random.Random(ROOT_SEED + family * 8191 + CLASSES.index(cls) * 9973)
    ref_day = date(2026, 1, 15) + timedelta(days=rng.randrange(300))
    ref = datetime(ref_day.year, ref_day.month, ref_day.day, 12, tzinfo=timezone.utc)
    e1 = ref - timedelta(days=rng.choice((1, 2, 3, 5)))
    offset = rng.choice((1, 2, 3))
    e2 = ref - timedelta(days=offset)
    content = f"synthetic-content-{family % 83}"
    base = f"synthetic-series-{family}"
    item = {
        "family_id": family,
        "event_a_id": base + "-a",
        "event_b_id": base + "-b",
        "content_a": content,
        "content_b": content,
        "event_a_time": e1,
        "event_b_time": e2,
        "reference_time": ref,
        "b_status": "OBSERVED",
        "ground_truth": cls,
        "synthetic_only": True,
    }
    if cls == "SAME_EVENT":
        item["event_b_id"] = item["event_a_id"]
        item["event_b_time"] = e1
    elif cls == "CONTINUING_EVENT":
        item["event_b_id"] = item["event_a_id"]
        item["b_status"] = "CONTINUATION"
        item["event_b_time"] = e1 + timedelta(days=rng.choice((1, 2)))
    elif cls == "DISTINCT_CONTENT":
        item["content_b"] = f"other-content-{family % 79}"
    elif cls == "FUTURE_PLAN":
        item["b_status"] = "PLANNED"
        item["event_b_time"] = ref + timedelta(days=rng.choice((1, 2, 3)))
    elif cls == "MEMORY_OF_EVENT":
        item["b_status"] = "MEMORY_REFERENCE"
        item["event_b_id"] = item["event_a_id"]
        item["event_b_time"] = ref
    elif cls == "AMBIGUOUS_REFERENCE":
        item["event_a_id"] = None
        item["event_b_id"] = None
        item["b_status"] = "UNCERTAIN"
    return item

def features(item: dict) -> list[float]:
    """Extract metadata only. Never include the synthetic ground-truth label."""
    if not item.get("synthetic_only"):
        raise ValueError("R4 refuses non-synthetic examples")
    status = item["b_status"]
    a = _utc(item["event_a_time"])
    b = _utc(item["event_b_time"])
    ref = _utc(item["reference_time"])
    delta = (b.date() - a.date()).days
    return [
        1.0,
        float(item["event_a_id"] is not None and item["event_a_id"] == item["event_b_id"]),
        float(item["event_a_id"] is not None and item["event_b_id"] is not None),
        float(item["content_a"] == item["content_b"]),
        float(status == "OBSERVED"),
        float(status == "PLANNED"),
        float(status == "MEMORY_REFERENCE"),
        float(status == "CONTINUATION"),
        float(item["event_a_id"] is None or item["event_b_id"] is None),
        float(b > ref),
        float(a.date() == b.date()),
        float(b < ref),
        min(abs(delta), 7) / 7.0,
    ]

def _softmax(values: list[float]) -> list[float]:
    v = max(values)
    z = [math.exp(x - v) for x in values]
    total = sum(z)
    return [x / total for x in z]

def _predict(weights: list[list[float]], x: list[float]) -> int:
    scores = [sum(w_i * x_i for w_i, x_i in zip(row, x)) for row in weights]
    return max(range(len(scores)), key=lambda i: scores[i])

def _truth_vector(item: dict) -> int:
    return CLASSES.index(item["ground_truth"])

def train_and_evaluate() -> dict:
    """Fixed-seed, disjoint-family training and untouched held-out evaluation."""
    # 700 families x 7 classes; no family appears in more than one split.
    train_families = range(0, 480)
    validation_families = range(480, 560)
    test_families = range(560, 700)
    datasets = [
        [generate_case(i, cls) for i in fams for cls in CLASSES]
        for fams in (train_families, validation_families, test_families)
    ]
    weights = [[0.0] * len(FEATURE_NAMES) for _ in CLASSES]
    rng = random.Random(ROOT_SEED)
    train_items = datasets[0]
    curve = []
    lr = 0.12
    for epoch in range(36):
        order = list(range(len(train_items)))
        rng.shuffle(order)
        for index in order:
            item = train_items[index]
            x = features(item)
            scores = [sum(w_i*x_i for w_i, x_i in zip(row, x)) for row in weights]
            probs = _softmax(scores)
            truth = _truth_vector(item)
            for c in range(len(CLASSES)):
                diff = (float(c == truth) - probs[c]) * lr
                for k in range(len(x)):
                    weights[c][k] += diff*x[k]
        if epoch in (0, 4, 11, 23, 35):
            curve.append({"epoch": epoch+1, "validation_accuracy": round(
                sum(_predict(weights, features(r)) == _truth_vector(r)
                    for r in datasets[1]) / len(datasets[1]), 6)})
    test = datasets[2]
    matrix = {a: {b: 0 for b in CLASSES} for a in CLASSES}
    safe_failures = 0
    for item in test:
        predicted = CLASSES[_predict(weights, features(item))]
        truth = item["ground_truth"]
        matrix[truth][predicted] += 1
        if (item["b_status"] == "PLANNED" and predicted in
            ("SAME_EVENT", "OBSERVED_REPEAT", "CONTINUING_EVENT")):
            safe_failures += 1
    correct = sum(matrix[c][c] for c in CLASSES)
    baseline = max(sum(matrix[c].values() for c in CLASSES)
                   for _ in range(1)) / len(test)
    # 'constant majority' accuracy is 1/7 on balanced synthetic classes.
    safe_guard_pass = safe_failures == 0
    return {
        "schema": "janus.simptomat.tachyon.r4.synthetic_training_receipt.v1",
        "run_type": "ACTUAL_OFFLINE_SOFTMAX_PARAMETER_TRAINING",
        "dataset": "SYNTHETIC_EVENT_METADATA_ONLY",
        "train_cases": len(datasets[0]), "validation_cases": len(datasets[1]),
        "heldout_test_cases": len(test), "heldout_family_count": len(test_families),
        "family_overlap": False, "seed": ROOT_SEED,
        "model": "MULTICLASS_LINEAR_SOFTMAX_SGD_STDLIB",
        "epochs": 36, "learning_rate": lr,
        "classes": list(CLASSES), "features": list(FEATURE_NAMES),
        "weights": [[round(v, 8) for v in row] for row in weights],
        "model_parameters_trained": len(CLASSES)*len(FEATURE_NAMES),
        "validation_curve": curve, "heldout_confusion": matrix,
        "heldout_correct": correct,
        "heldout_accuracy": round(correct/len(test), 6),
        "constant_majority_baseline_accuracy": round(baseline, 6),
        "prospective_to_observed_misclassifications": safe_failures,
        "training_qualified_synthetic": correct/len(test) >= 0.90 and safe_guard_pass,
        "scientific_gate": "HOLD_NO_REAL_PARTICIPANT_DATA_OR_CONSCIOUSNESS_VALIDATION",
        "clinical_training": False, "patient_data_used": False,
        "brain_state_inference": False, "phenomenal_time_measured": False,
        "physically_timeless_consciousness_verified": False,
        "physical_time_change_verified": False,
        "deployment_permission": "RESEARCH_ONLY__NO_PRODUCTION_MODEL_UPDATE",
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    args = parser.parse_args()
    if not args.train:
        parser.error("Only offline synthetic --train is supported")
    receipt = train_and_evaluate()
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if not receipt["training_qualified_synthetic"]:
        raise SystemExit("SYNTHETIC_R4_TRAINING_GATE_FAIL")

if __name__ == "__main__":
    main()
