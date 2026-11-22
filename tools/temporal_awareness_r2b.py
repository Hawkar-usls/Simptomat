"""R2B independent-methods audit of the fixed synthetic R1 classifier.

Only a complete mathematical count grid is accepted. This module has no data
reader, network client, clinical prediction, model training or live interface.
The toy forward model demonstrates structural non-identifiability under stated
assumptions; label boundary fragility is a separate software property.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import itertools
import json
import math
import random
import statistics

from tools.temporal_awareness_r2 import score_vector
from tools.temporal_awareness_lab import TRIAL_KEYS
from tools.temporal_awareness_r2b_power import report as power_report


GRID = tuple(itertools.product(range(6), repeat=4))
GRID_INDEX = {point: index for index, point in enumerate(GRID)}
SEEDS = (1729, 2718, 31415, 42424, 65537, 104729, 130363, 196613)
SCIENCE_GATE = "HOLD_NO_INDEPENDENT_PARTICIPANT_LEVEL_VALIDATION"
SEQUENCE = "SEQUENCE_SPECIFIC_DISSOCIATION_CANDIDATE"
DELAYED = "DELAYED_RECALL_SPECIFIC_DISSOCIATION_CANDIDATE"
MIXED = "MIXED_SEQUENCE_AND_DELAYED_RECALL_DISSOCIATION_CANDIDATE"
NO_DEMO = "NO_DEMO_DISSOCIATION"
ENGAGEMENT = "INDETERMINATE_ONLINE_ENGAGEMENT_CONFOUND"
ENCODING = "INDETERMINATE_IMMEDIATE_ENCODING_CONFOUND"
MIDRANGE = "INDETERMINATE_MIXED_OR_MIDRANGE"
CANDIDATES = frozenset((SEQUENCE, DELAYED, MIXED))
CLASSES = tuple(sorted((*CANDIDATES, NO_DEMO, ENGAGEMENT, ENCODING, MIDRANGE)))


def _check_counts(counts: tuple[int, ...]) -> None:
    if (not isinstance(counts, tuple) or len(counts) != 4
            or any(type(x) is not int or not 0 <= x <= 5 for x in counts)):
        raise ValueError("exactly four synthetic integer counts in 0..5 required")


def threshold_verdict(counts: tuple[int, ...], low: int = 1, high: int = 4) -> str:
    """Research copy for sensitivity only; never changes R1 thresholds."""
    _check_counts(counts)
    if (type(low) is not int or type(high) is not int
            or not 0 <= low < high <= 5):
        raise ValueError("synthetic threshold pair must satisfy 0 <= low < high <= 5")
    engagement, recognition, sequence, recall = counts
    if engagement < high:
        return ENGAGEMENT
    if recognition < high:
        return ENCODING
    if sequence <= low and recall >= high:
        return SEQUENCE
    if sequence >= high and recall <= low:
        return DELAYED
    if sequence <= low and recall <= low:
        return MIXED
    if sequence >= high and recall >= high:
        return NO_DEMO
    return MIDRANGE


def directed_edges() -> tuple[tuple[int, int], ...]:
    """All legal directed +/-1 neighbors; each undirected edge occurs twice."""
    edges = []
    for source, point in enumerate(GRID):
        for axis in range(4):
            for delta in (-1, 1):
                value = point[axis] + delta
                if 0 <= value <= 5:
                    target = point[:axis] + (value,) + point[axis + 1:]
                    edges.append((source, GRID_INDEX[target]))
    return tuple(edges)


EDGES = directed_edges()


def boundary_metrics(labels: list[str] | tuple[str, ...]) -> dict:
    if len(labels) != len(GRID):
        raise ValueError("one frozen label per synthetic grid vertex required")
    unstable = set()
    flips = 0
    for source, target in EDGES:
        if labels[source] != labels[target]:
            flips += 1
            unstable.add(source)
    return {
        "directed_neighbor_comparisons": len(EDGES),
        "directed_label_flips": flips,
        "flip_fraction": flips / len(EDGES),
        "unstable_vectors": len(unstable),
        "unstable_fraction": len(unstable) / len(GRID),
        "stable_vectors": len(GRID) - len(unstable),
        "class_counts": dict(sorted(Counter(labels).items())),
    }


def r1_reproduction() -> dict:
    """Invoke the actual frozen R1 code, rather than just the sensitivity copy."""
    labels = [score_vector(point)["verdict"] for point in GRID]
    metrics = boundary_metrics(labels)
    tally = Counter(labels)
    candidates = sum(tally[label] for label in CANDIDATES)
    indeterminate = sum(n for label, n in tally.items() if label.startswith("INDETERMINATE_"))
    return {
        "grid_vectors": len(GRID),
        **metrics,
        "dissociation_candidate_vectors": candidates,
        "indeterminate_vectors": indeterminate,
        "no_demo_dissociation_vectors": tally[NO_DEMO],
        "noncandidate_vectors": len(GRID) - candidates,
        "candidate_fraction_synthetic_grid_only": candidates / len(GRID),
        "review_correction": "1296-48=1248 noncandidates: 1232 indeterminate plus 16 NO_DEMO_DISSOCIATION",
        "unit_test_correction": "Historical R1+R2 total 36 means software unit tests, not 36 clinical hypotheses",
        "clinical_prevalence_estimate": None,
    }


def _random_control_summary(samples: list[dict]) -> dict:
    fractions = [sample["flip_fraction"] for sample in samples]
    return {
        "seeds": list(SEEDS),
        "samples": samples,
        "mean_flip_fraction": statistics.mean(fractions),
        "minimum_flip_fraction": min(fractions),
        "maximum_flip_fraction": max(fractions),
        "standard_deviation_between_seed_runs": statistics.stdev(fractions),
        "interval_interpretation": "Fixed-seed engineering controls, not confidence intervals or independent scientific replications",
    }


def baseline_comparison() -> dict:
    fixed_labels = [score_vector(point)["verdict"] for point in GRID]
    histogram = Counter(fixed_labels)
    uniform_runs, shuffled_runs = [], []
    for seed in SEEDS:
        rng = random.Random(seed)
        # Freeze the complete label map before looking at any edge; do not draw
        # a new label every time the same vertex is encountered.
        uniform = [CLASSES[rng.randrange(len(CLASSES))] for _ in GRID]
        uniform_runs.append({"seed": seed, **boundary_metrics(uniform)})
        shuffled = fixed_labels.copy()
        random.Random(seed).shuffle(shuffled)
        shuffled_runs.append({"seed": seed, **boundary_metrics(shuffled)})
    n = len(GRID)
    iid_matched = 1 - sum((count / n) ** 2 for count in histogram.values())
    # The permutation fixes all class counts. Distinct vertices are sampled
    # without replacement, so P(different) = 1-sum n_k(n_k-1)/(N(N-1)).
    permutation_expected = 1 - sum(count * (count - 1) for count in histogram.values()) / (n * (n - 1))
    return {
        "metric": "Fixed-label boundary changes on exactly the same 8640 directed grid edges",
        "interpretation": "Stability depends on label geometry and class imbalance. These controls provide context, not validity, accuracy, acceptable error or a clinical optimum.",
        "oracle_ceiling": "NOT_DEFINED_NO_INDEPENDENT_GROUND_TRUTH",
        "constant": boundary_metrics(["CONSTANT"] * n),
        "one_feature_threshold": {
            "definition": "online_engagement >= 4, binary synthetic control",
            **boundary_metrics(["HIGH" if point[0] >= 4 else "OTHER" for point in GRID]),
        },
        "uniform_seven_class_iid": {
            "expected_flip_fraction": 1 - 1 / len(CLASSES),
            "expectation_formula": "1 - sum_k p_k^2, p_k=1/7",
            **_random_control_summary(uniform_runs),
        },
        "r1_histogram_preserving_random_permutation": {
            "expected_flip_fraction": permutation_expected,
            "expectation_formula": "1 - sum_k n_k*(n_k-1)/(N*(N-1)), distinct vertices; no replacement",
            "iid_same_marginal_comparison_only": iid_matched,
            "class_counts_preserved_exactly": dict(sorted(histogram.items())),
            **_random_control_summary(shuffled_runs),
        },
        "randomization_limits": "Grid edges share vertices and opposite directions duplicate each edge; 8640 comparisons are not independent Bernoulli trials. No binomial CI or p-value is assigned to flip rates.",
    }


def threshold_sensitivity() -> dict:
    base_labels = [threshold_verdict(point) for point in GRID]
    base_members = {index for index, label in enumerate(base_labels) if label in CANDIDATES}
    base_per_class = {label: {index for index, value in enumerate(base_labels) if value == label} for label in CANDIDATES}
    rows = []
    for low in range(5):
        for high in range(low + 1, 6):
            labels = [threshold_verdict(point, low, high) for point in GRID]
            members = {index for index, label in enumerate(labels) if label in CANDIDATES}
            union = members | base_members
            changed = sum(a != b for a, b in zip(base_labels, labels))
            row = {
                "low_at_most": low,
                "high_at_least": high,
                **boundary_metrics(labels),
                "candidate_vectors": len(members),
                "candidate_fraction_synthetic_grid_only": len(members) / len(GRID),
                "candidate_membership_vs_r1": {
                    "retained": len(members & base_members),
                    "lost": len(base_members - members),
                    "new": len(members - base_members),
                    "jaccard": len(members & base_members) / len(union) if union else 1.0,
                },
                "label_changes_vs_r1": changed,
                "per_candidate_class_membership_vs_r1": {},
            }
            for label in sorted(CANDIDATES):
                selected = {index for index, value in enumerate(labels) if value == label}
                original = base_per_class[label]
                row["per_candidate_class_membership_vs_r1"][label] = {
                    "retained": len(selected & original),
                    "lost": len(original - selected),
                    "new": len(selected - original),
                }
            rows.append(row)
    return {
        "base_low_at_most": 1,
        "base_high_at_least": 4,
        "grid": "All 15 integer threshold pairs 0 <= LOW < HIGH <= 5, same fixed 1296 vectors",
        "R1_implementation_modified": False,
        "selection_rule": "Exhaustive reporting; no post-hoc best threshold selected",
        "rows": rows,
        "candidate_count_range": [min(r["candidate_vectors"] for r in rows), max(r["candidate_vectors"] for r in rows)],
        "interpretation": "Candidate numbers AND membership depend on arbitrary demo thresholds; not merely their clinical interpretation. Synthetic-grid fractions are not population prevalences.",
    }


def forward_probabilities(capacity: tuple[int, ...], task_access: tuple[int, ...]) -> tuple[Fraction, ...]:
    """Toy generative map: P(correct_j)=(capacity_j/5)*(access_j/5).

    A capacity factor and an independent task-access gate must both succeed.
    No neuroscientific validity is asserted for this hypothetical factorization.
    """
    _check_counts(capacity)
    _check_counts(task_access)
    return tuple(Fraction(a * b, 25) for a, b in zip(capacity, task_access))


def observation_mass(counts: tuple[int, ...], probabilities: tuple[Fraction, ...]) -> Fraction:
    """Exact full-vector PMF under five independent trials per independent task."""
    _check_counts(counts)
    if (len(probabilities) != 4 or any(not isinstance(p, Fraction) or not 0 <= p <= 1 for p in probabilities)):
        raise ValueError("four exact rational probabilities in [0,1] required")
    mass = Fraction(1)
    for count, probability in zip(counts, probabilities):
        mass *= math.comb(5, count) * probability ** count * (1 - probability) ** (5 - count)
    return mass


def _rational(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def constructive_nonidentifiability() -> dict:
    witnesses = []
    for target in ((5, 5, 1, 5), (5, 5, 0, 4), (4, 5, 1, 4),
                   (5, 5, 5, 1), (5, 4, 4, 0), (5, 5, 1, 1)):
        full = (5, 5, 5, 5)
        a, b = (target, full), (full, target)
        p_a, p_b = forward_probabilities(*a), forward_probabilities(*b)
        mass_a, mass_b = observation_mass(target, p_a), observation_mass(target, p_b)
        witnesses.append({
            "latent_A": {"capacity_fifths": list(a[0]), "task_access_fifths": list(a[1])},
            "latent_B": {"capacity_fifths": list(b[0]), "task_access_fifths": list(b[1])},
            "latent_states_distinct": a != b,
            "same_forward_probabilities": p_a == p_b,
            "per_task_success_probabilities_exact": [_rational(p) for p in p_a],
            "identical_observation_counts": list(target),
            "observed_R1_label": score_vector(target)["verdict"],
            "exact_observation_probability_A": _rational(mass_a),
            "exact_observation_probability_B": _rational(mass_b),
            "positive_identical_observation_probability": mass_a == mass_b and mass_a > 0,
        })
    return {
        "type": "CONSTRUCTIVE_MANY_TO_ONE_FORWARD_MODEL",
        "task_order": list(TRIAL_KEYS),
        "latent_space": "Two distinct 4-tuples of capacity and task-access probabilities, each in {0,1/5,...,1}",
        "forward_map": "p_j = capacity_j * task_access_j; Y_j ~ Binomial(5,p_j), tasks independent",
        "proof": "For any q != (1,1,1,1), latent A=(capacity=q, access=1) and latent B=(capacity=1, access=q) differ but produce the same p=q. Therefore P_A(Y=y)=P_B(Y=y) for every y in {0,...,5}^4, not just the displayed witness. The observable-distribution map is noninjective.",
        "assumptions": [
            "Each correct answer requires both a capacity factor and a task-access factor, with multiplicative success probability",
            "Five independent, identically distributed Bernoulli trials per task and independence across tasks",
            "Neither latent factor is directly measured or experimentally isolated by the four counters",
            "This hypothetical model class is admitted for the logical counterexample only; it is not a validated model of any participant or disease",
        ],
        "witnesses": witnesses,
        "all_witnesses_same_forward_distribution": all(w["same_forward_probabilities"] and w["latent_states_distinct"] for w in witnesses),
        "claim_ceiling": "Counts alone cannot identify the factors within this admitted toy model class; this does not prove which mechanisms exist in people or that no richer study can identify them",
        "distinct_observable_vectors_used_as_nonidentifiability_proof": False,
        "flip_statistics_used_as_nonidentifiability_proof": False,
        "additional_identification_requirements": "Independent measurements or interventions isolating task access/capacity, and independently justified structural assumptions",
    }


def audit() -> dict:
    return {
        "schema": "simptomat.tachyon.r2b.independent_methods.synthetic_audit.v1",
        "artifact_id": "JANUS-TACHYON-SIMPTOMAT-R2B-INDEPENDENT-METHODS-2026-11-22",
        "created_on": "2026-11-22",
        "status": "SYNTHETIC_AUDIT_GENERATED__SCIENTIFIC_HOLD",
        "engineering_status_scope": "Generated deterministic methods artifact; actual engineering validation requires tests, exact replay and remote CI with commit/run URL reported separately",
        "review_scope": "Methods response to the external document review; independent code checks are not independent human data or independent clinical replication",
        "source": "COMPLETE_ENUMERATION_0_TO_5__NO_HUMAN_DATA",
        "R1_classifier_unchanged": True,
        "r1_reproduction": r1_reproduction(),
        "baseline_comparison": baseline_comparison(),
        "threshold_sensitivity": threshold_sensitivity(),
        "constructive_nonidentifiability": constructive_nonidentifiability(),
        "power_analysis": power_report(),
        "scientific_gate": SCIENCE_GATE,
        "claim_ceiling": "SYNTHETIC_METHODS_ONLY__NO_CLINICAL_OR_PHYSICAL_PROMOTION",
        "human_data_analyzed": False,
        "patient_data_ingested": False,
        "independent_clinical_replication": False,
        "clinical_validation": False,
        "live_screening_enabled": False,
        "production_model_weights_changed": False,
        "timeless_consciousness_proven": False,
        "physical_time_travel_proven": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="R2B fixed-grid synthetic methods audit; no human input supported")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if not args.audit:
        parser.error("only --audit is supported; no participant-data ingestion")
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
