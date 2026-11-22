"""Prospective paired-contrast power planning; no human inputs or prevalence model.

The paired t-test power is computed by deterministic quadrature of its
noncentral-t representation T=(Z+d*sqrt(n))/sqrt(V/(n-1)), with independent
Z~N(0,1), V~chi-square(n-1). This is numerical model power, not empirical power.
Only fixed hypothetical design assumptions are evaluated by the CLI.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math


def _beta_fraction(a: float, b: float, x: float) -> float:
    """Continued fraction for regularized incomplete beta, modified Lentz."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1 / d
    h = d
    for m in range(1, 401):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d, c = 1 + aa * d, 1 + aa / c
        if abs(d) < tiny:
            d = tiny
        if abs(c) < tiny:
            c = tiny
        d = 1 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d, c = 1 + aa * d, 1 + aa / c
        if abs(d) < tiny:
            d = tiny
        if abs(c) < tiny:
            c = tiny
        d = 1 / d
        change = d * c
        h *= change
        if abs(change - 1) < 3e-14:
            return h
    raise ArithmeticError("incomplete beta did not converge")


def _regularized_beta(x: float, a: float, b: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                     + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return front * _beta_fraction(a, b, x) / a
    return 1 - front * _beta_fraction(b, a, 1 - x) / b


@lru_cache(maxsize=512)
def t_critical(n: int, alpha: float = 0.025) -> float:
    """Positive central t cutoff for a two-sided paired test with n pairs."""
    if type(n) is not int or n < 2 or not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("n>=2 and 0<alpha<1 required")
    df = n - 1

    def upper_tail(t: float) -> float:
        return 0.5 * _regularized_beta(df / (df + t * t), df / 2, 0.5)

    low, high = 0.0, 1.0
    while upper_tail(high) > alpha / 2:
        high *= 2
    for _ in range(60):
        middle = (low + high) / 2
        if upper_tail(middle) > alpha / 2:
            low = middle
        else:
            high = middle
    return (low + high) / 2


@lru_cache(maxsize=1024)
def paired_t_power(n: int, effect_dz: float, alpha: float = 0.025,
                   steps: int = 4096) -> float:
    """Two-sided paired t power under independent normally distributed D_i.

    Integrate over U=sqrt(V/df). Simpson quadrature is deterministic. The
    finite upper bound leaves negligible chi-square tail mass for this report's
    df; convergence is verified against twice as many panels in software tests.
    """
    if (type(n) is not int or not 2 <= n <= 100000
            or not math.isfinite(effect_dz) or abs(effect_dz) > 10
            or not math.isfinite(alpha) or not 0 < alpha < 1
            or type(steps) is not int or steps < 256 or steps % 2):
        raise ValueError("invalid paired t power design")
    df = n - 1
    cutoff = t_critical(n, alpha)
    noncentrality = abs(effect_dz) * math.sqrt(n)
    upper = max(4.0, 1 + 12 / math.sqrt(2 * df))
    width = upper / steps
    log_constant = math.log(2) + (df / 2) * math.log(df / 2) - math.lgamma(df / 2)

    def integrand(u: float) -> float:
        if u == 0:
            density = math.exp(log_constant) if df == 1 else 0.0
        else:
            density = math.exp(log_constant + (df - 1) * math.log(u) - df * u * u / 2)
        rejection = (0.5 * math.erfc((cutoff * u - noncentrality) / math.sqrt(2))
                     + 0.5 * math.erfc((cutoff * u + noncentrality) / math.sqrt(2)))
        return density * rejection

    total = integrand(0.0) + integrand(upper)
    total += sum((4 if k % 2 else 2) * integrand(k * width) for k in range(1, steps))
    return min(1.0, max(0.0, width * total / 3))


def required_pairs(effect_dz: float, target_power: float = 0.9,
                   alpha: float = 0.025) -> int:
    if (not math.isfinite(effect_dz) or not 0 < effect_dz <= 10
            or not math.isfinite(target_power) or not alpha < target_power < 1):
        raise ValueError("positive effect and alpha<target<1 required")
    low, high = 2, 4
    while paired_t_power(high, effect_dz, alpha) < target_power:
        high *= 2
        if high > 100000:
            raise ValueError("design exceeds supported planning range")
    while low < high:
        middle = (low + high) // 2
        if paired_t_power(middle, effect_dz, alpha) >= target_power:
            high = middle
        else:
            low = middle + 1
    return low


def recruitment_plan(holdout_pairs: int, holdout_fraction: float = 0.4,
                     attrition: float = 0.2) -> dict:
    """Expected retention inflation, not a probability guarantee of final N."""
    if (type(holdout_pairs) is not int or holdout_pairs < 2
            or not math.isfinite(holdout_fraction) or not 0 < holdout_fraction < 1
            or not math.isfinite(attrition) or not 0 <= attrition < 1):
        raise ValueError("invalid allocation or attrition")
    complete = math.ceil(holdout_pairs / holdout_fraction)
    return {"evaluable_holdout_pairs": holdout_pairs,
            "total_evaluable_participants": complete,
            "development_participants": complete - holdout_pairs,
            "recruitment_target_expected_retention": math.ceil(complete / (1 - attrition)),
            "holdout_fraction": holdout_fraction, "assumed_attrition_fraction": attrition}


def report() -> dict:
    scenarios = []
    for effect in (0.2, 0.3, 0.5):
        for target in (0.8, 0.9):
            n = required_pairs(effect, target)
            scenarios.append({"assumed_dz": effect, "target_marginal_power": target,
                              "two_sided_alpha_per_endpoint": 0.025,
                              "numerical_power_at_n": round(paired_t_power(n, effect), 9),
                              "numerical_power_at_n_minus_one": round(paired_t_power(n - 1, effect), 9),
                              "both_endpoints_power_lower_bound": round(max(0.0, 2 * target - 1), 6),
                              **recruitment_plan(n)})
    selected = next(s for s in scenarios if s["assumed_dz"] == 0.3
                    and s["target_marginal_power"] == 0.9)
    return {
        "schema": "simptomat.tachyon.r2b.prospective_power.v1",
        "status": "HYPOTHETICAL_PLANNING_ONLY__NO_PARTICIPANT_DATA",
        "endpoint_unit": "ONE_INDEPENDENT_PARTICIPANT_WITH_COMPLETE_PAIRED_TASK_SCORES",
        "model": "T=(Z+dz*sqrt(n))/sqrt(V/(n-1)); Z normal, V chi-square, independent",
        "calculation": "Noncentral paired-t power via stdlib Simpson quadrature; 4096 panels",
        "effect_definition": "dz=population mean within-person standardized-task difference / SD of that difference",
        "primary_contrasts": ["Z_immediate_recognition - Z_temporal_order - b_order_external_eligible_reference",
                              "Z_immediate_recognition - Z_delayed_recall - b_recall_external_eligible_reference"],
        "nulls": ["E[D_order]=0", "E[D_recall]=0"],
        "assumptions": [
            "Independent participants; normally distributed participant-level paired differences",
            "External fixed task norms on comparable scales; higher Z means better performance",
            "Fixed external expected contrasts b_order/b_recall calibrated under the identical eligibility rule remove ordinary task and eligibility-induced mismatch",
            "The hypothetical dz values are assumptions, not estimates from R1/R2 or literature p-values",
            "Within-person trials are not independent sample-size units; trial dependence is absorbed in SD(D)",
            "No site/family clustering; clustered recruitment requires redesign and new power analysis",
            "20% missing or excluded pairs and 40% holdout are planning assumptions, not guaranteed retention",
            "No selection on order or delayed-recall outcomes; eligibility uses independent engagement/recognition checks",
        ],
        "multiplicity": {"confirmatory_family_size": 2, "analysis": "Holm step-down FWER 0.05",
                         "planning": "Bonferroni two-sided alpha=0.025 each",
                         "software_unit_tests_are_statistical_hypotheses": False,
                         "joint_power": "If both endpoints meet at least 90% marginal power, union bound gives at least 80% both-reject power, without assuming endpoint independence"},
        "scenarios": scenarios,
        "illustrative_selected_design": selected,
        "selected_design_is_final_recruitment_authorization": False,
        "sensitivity": {"holdout_fraction_0_3": recruitment_plan(selected["evaluable_holdout_pairs"], 0.3, 0.2),
                        "attrition_0_3": recruitment_plan(selected["evaluable_holdout_pairs"], 0.4, 0.3)},
        "synthetic_candidate_grid_fraction_used_as_prevalence": False,
        "prevalence_test_against_zero_used": False,
        "zero_null_caveat": "Seeing >=1 event rejects an error-free p=0 model trivially; that is not clinical sensitivity, prevalence validation, or a meaningful planning alternative here",
        "limits": ["No clinical effect, prevalence, trial reliability, missingness mechanism or variance has been estimated",
                   "The powered primary contrasts do not establish individual selective dissociation or causal mechanism",
                   "Small accessible archival cohorts may support only exploratory feasibility with uncertainty, never a lowered evidentiary gate",
                   "Final source-specific design must freeze instruments, external norms, eligibility, feasible N and deviations before any outcome access"],
        "patient_data_used": False, "clinical_validation": False,
        "scientific_gate": "HOLD_NO_INDEPENDENT_PARTICIPANT_LEVEL_VALIDATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fixed hypothetical R2B power planning; no participant input")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if not args.audit:
        parser.error("only --audit is supported")
    print(json.dumps(report(), ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
