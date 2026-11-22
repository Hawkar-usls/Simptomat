"""TACHYON×Simptomat R2: exhaustive synthetic identifiability and fragility audit.

Not a dementia diagnostic, not a consciousness test, not a time-travel test.
The full count grid consists of mathematical 0..5 task-count vectors,
NOT participant recordings. Published numbers are cited, never reanalyzed as
if individual-level data were supplied.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter

from tools.temporal_awareness_lab import (
    TRIAL_KEYS, synthetic_case, evaluate_fixture,
)

N_SYNTHETIC_VECTORS = 6 ** len(TRIAL_KEYS)
SCIENTIFIC_GATE = "HOLD_NO_INDEPENDENT_PARTICIPANT_LEVEL_VALIDATION"
PUBLISHED_PAPER_NON_SIGNIFICANT_P = 0.15


def score_vector(counts: tuple[int, int, int, int], *, felt_no_time_flow: bool = True) -> dict:
    """Apply unchanged, pre-existing R1 rules to four artificial task counts."""
    if (not isinstance(counts, tuple) or len(counts) != len(TRIAL_KEYS)
            or any(type(x) is not int or x < 0 or x > 5 for x in counts)):
        raise ValueError("4 counts (0..5) required, synthetic only")
    rec = synthetic_case("NO_DISSOCIATION", felt_no_time_flow=felt_no_time_flow)
    for key, value in zip(TRIAL_KEYS, counts):
        rec["tasks"][key]["correct"] = value
    return evaluate_fixture(rec)


def wilson_interval(success: int, total: int = 5, z: float = 1.96) -> tuple[float, float]:
    """Illustrative interval for an independent Bernoulli-trial idealization.

    Five trials per task are too few for a clinically validated assessment;
    real testing could violate trial independence and need a different model.
    """
    if (type(success) is not int or type(total) is not int or total < 1
            or not 0 <= success <= total or not math.isfinite(z) or z <= 0):
        raise ValueError("bad binomial interval inputs")
    p = success / total
    zz = z*z
    den = 1 + zz/total
    mid = (p + zz/(2*total))/den
    rad = (z/den) * math.sqrt((p*(1-p) + zz/(4*total))/total)
    return max(0.0, mid-rad), min(1.0, mid+rad)


def _verdict(counts: tuple[int, int, int, int]) -> str:
    return score_vector(counts)["verdict"]


def ambiguity_demo() -> dict:
    counts = (5, 5, 1, 5)
    outcome = score_vector(counts)
    # Two alternative CAUSAL STORIES have exactly the same observable profile.
    # They are thought experiments, not synthetic labels given to the model.
    latent_stories = (
        "ORDER_ENCODING_SPECIFIC_PROBLEM",
        "TASK_STRATEGY_OR_SENSORY_SEQUENCING_CONFOUND",
    )
    same_observation = all(_verdict(counts) == outcome["verdict"] for _ in latent_stories)
    return {
        "observed_task_counts": dict(zip(TRIAL_KEYS, counts)),
        "possible_competing_causes": list(latent_stories),
        "observed_pattern": outcome["verdict"],
        "same_observables_under_competing_causes": same_observation,
        "causal_mechanism_identifiable_from_four_counts": False,
        "first_person_timelessness_proven": False,
        "scientific_interpretation": "Descriptive pattern only, neither pathophysiology nor subjective timelessness established",
    }


def audit() -> dict:
    counts: Counter[str] = Counter()
    neighbors = 0
    changed = 0
    robust = 0
    unacceptable = 0
    nonclinical_broken = 0
    for vector in itertools.product(range(6), repeat=len(TRIAL_KEYS)):
        result = score_vector(vector)
        verdict = result["verdict"]
        counts[verdict] += 1
        if verdict.startswith("REJECT"):
            unacceptable += 1
        if (result["alzheimer_status"] != "NOT_EVALUATED"
                or result["clinical_diagnosis"] != "NOT_EVALUATED"
                or result["consciousness_status"] != "NOT_ESTABLISHED"
                or result["physical_time_travel_proven"]
                or result["timeless_consciousness_proven"]):
            nonclinical_broken += 1
        touched = False
        for index in range(len(vector)):
            for difference in (-1, 1):
                new = vector[index] + difference
                if not 0 <= new <= 5:
                    continue
                sibling = vector[:index] + (new,) + vector[index+1:]
                neighbors += 1
                flip = _verdict(sibling) != verdict
                changed += int(flip)
                touched = touched or flip
        robust += int(not touched)
    low_ci = wilson_interval(1)
    high_ci = wilson_interval(4)
    overlap = max(low_ci[0], high_ci[0]) <= min(low_ci[1], high_ci[1])
    return {
        "schema": "simptomat.tachyon.r2.identifiability.synthetic_audit.v1",
        "source": "COMPLETE_ENUMERATION_0_TO_5__NO_HUMAN_DATA",
        "R1_classifier_unchanged": True,
        "R1_total_vectors": N_SYNTHETIC_VECTORS,
        "profiles_by_R1_descriptive_verdict": dict(sorted(counts.items())),
        "invalid_synthetic_vectors": unacceptable,
        "scientific_guard_violations": nonclinical_broken,
        "neighbors_comparisons_directed": neighbors,
        "neighbor_label_flips_directed": changed,
        "neighbor_flip_fraction": round(changed/neighbors, 6),
        "one_point_stable_vectors": robust,
        "one_point_unstable_vectors": N_SYNTHETIC_VECTORS-robust,
        "demonstrative_five_trial_uncertainty": {
            "assumption": "INDIVIDUAL_BERNOULLI_TRIAL_INDEPENDENCE_UNVERIFIED_AND_NOT_CLINICAL",
            "one_of_five_wilson95": [round(x, 6) for x in low_ci],
            "four_of_five_wilson95": [round(x, 6) for x in high_ci],
            "intervals_overlap": overlap,
            "implication": "Pre-set R1 HIGH/LOW labels cannot be treated as proven distinct patient-level capabilities",
        },
        "causal_identifiability_counterexample": ambiguity_demo(),
        "two_distinct_descriptive_cases": {
            "poor_order_good_delayed_recall": _verdict((5,5,1,5)),
            "good_order_poor_delayed_recall": _verdict((5,5,5,1)),
        },
        "literature_sanity": {
            "article_doi": "10.12779/dnd.2023.22.4.148",
            "reported_temporal_window_group_p": PUBLISHED_PAPER_NON_SIGNIFICANT_P,
            "statistically_significant_at_p_below_0_05": False,
            "disclaimer": "Published group result, not a new R2 analysis of individual participant data.",
            "additional_paper_doi": "10.1038/s41598-023-49222-x",
            "additional_paper_data_availability": "ON_REASONABLE_REQUEST_NOT_OBTAINED",
        },
        "scientific_gate": SCIENTIFIC_GATE,
        "claim_ceiling": "SYNTHETIC_METHOD_CHECK_ONLY__CAUSAL_NEURAL_STATE_NOT_IDENTIFIED",
        "physical_time_travel_proven": False,
        "timeless_consciousness_proven": False,
        "clinical_validation": False,
        "patient_data_used": False,
        "live_simptomat_interface_modified": False,
        "production_model_weights_updated": False,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Simptomat TACHYON R2 exhaustive synthetic audit")
    ap.add_argument("--audit", action="store_true")
    args = ap.parse_args()
    if not args.audit:
        ap.error("Only --audit is supported; no real patient input")
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
