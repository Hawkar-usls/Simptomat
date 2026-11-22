# TACHYON × Simptomat R2B — independent methods review response

Date: 2026-11-22. Scope: the external methods review supplied by the user in
ChatGPT conversation `6b0220ea-c7f4-83ed-86dd-2e1c62ada3a4`, latest user review
turn `5636622e-a681-47be-8493-6c99cc68905c`. The reviewer explicitly reviewed the
R2 document without checking code. R2B is an auditable response and separately
implemented methods checks; it is not independent clinical replication or a
claim that a human external reviewer audited this implementation.

## Corrections to the review

1. The complete grid is **1296**, not 1269: `(0..5)^4`.
   There are 48 dissociation candidates (16 sequence-specific, 16 delayed-recall
   specific, 16 mixed), 1232 indeterminate vectors and 16 `NO_DEMO_DISSOCIATION`.
   Thus **1296 − 48 = 1248 noncandidates = 1232 + 16**, not 1232 remaining vectors.
2. **36 was the R1 + R2 software unit-test count** (20 + 16), not 36 clinical
   hypotheses. Unit tests receive no multiplicity correction. The prospective
   study specifies its own two-hypothesis confirmatory family and Holm correction.
3. A label flip is a boundary property of a classifier on an artificial graph.
   Neither 704/8640 flips nor 532 unstable vectors proves non-identifiability.
   Two *different* observable vectors are also not such a proof.
4. Random controls do not generally approach 100% flips. For independent labels
   with probabilities `p_k`, expected disagreement is `1 − sum(p_k**2)`. A
   permutation preserving finite label counts has a different, explicit
   without-replacement expectation. R2B reports both controls and their seeds.
5. No oracle ceiling is available without independently established target
   truth and a justified noise model. No such ceiling, diagnostic accuracy,
   ranking of scientific merit or inferred true mechanism is reported.
6. **48/1296 = 3.7037% is synthetic grid occupancy**, not clinical prevalence,
   incidence, effect size or participant sampling probability. It cannot set N
   for a real study. The paired-endpoint power scenarios use stated hypothetical
   standardized effects and participant variance instead.

## Constructive non-identifiability

The new executable forward model maps latent capacity and task access to
observable success probabilities. Distinct latent factor assignments have the
same products and therefore the same complete count distribution under the
explicit toy independent-binomial assumption. Six witnesses show distinct
latent inputs with identical observable output; the check covers all 1296
possible observations, not merely a shared category label. The analytic product
identity establishes equality of distributions; enumeration checks the code.

This proves a many-to-one mapping **inside the stated toy model class**. It does
not demonstrate that either hypothetical mechanism exists in people, identify
neural causes, or establish an unrestricted impossibility theorem for all future
measurements. Additional justified measurements or interventions could break
the ambiguity. Observable engagement, immediate recognition, event order,
delayed memory, subjective duration and external physical time remain separate.

## Baselines and threshold sensitivity

All controls use the same 1296 vertices and 8640 **directed** ±1 edges. Reverse
edges repeat the same comparison: there are 4320 undirected edges, so the 8640
comparisons are not independent statistical observations. Exact enumeration
needs no sampling confidence interval or significance test for this grid.

The constant baseline supplies the 0% stability reference. One-feature threshold
controls show how much fragility arises from a single boundary. Uniform seeded
labels and seeded permutations of the R1 label histogram supply geometry and
class-imbalance controls. Seeds, realized counts, expectations and run-to-run
summaries are saved. These comparisons contextualize 8.1481%; they do not make
a low flip rate evidence of useful accuracy. A constant classifier illustrates
why stability alone is insufficient.

R2B exhaustively sweeps every integer `0 <= LOW < HIGH <= 5`, including R1
`LOW=1, HIGH=4`, without changing R1. For each setting it saves category counts,
candidate occupancy, edge flips, unstable vertices, and retained/lost/new
candidate sets plus Jaccard overlap relative to R1. This is a sensitivity audit,
not optimization of thresholds. No cutoff is selected by maximizing synthetic
candidate counts or minimizing flips. All clinical cutoffs remain unvalidated.

## Prospective research and power

The [prospective plan](TACHYON_R2B_PREREGISTRATION.md) and its
[machine-readable contract](../research/temporal_awareness/SIMPTOMAT_TACHYON_R2B_PREREGISTRATION_2026-11-22.json)
define two paired primary endpoints, the confirmatory family, holdout, missing
data rules, independent measurement and source gates. A primary contrast alone
does not establish a sequence-specific or recall-specific individual pattern.
The stronger operational pattern criteria also require separately assessed
engagement, immediate recognition and preservation of the nontarget task.

Power calculations distinguish participants from repeated trials, explicitly
state effect sizes, variance assumptions, alpha, power, holdout allocation and
attrition. They compute model-based noncentral paired-t power by numerical
quadrature under normally distributed participant differences. These provisional
assumptions do not guarantee a clinical sample size. Final instrument reliability and variance estimates require an
authorized development stage and a versioned freeze before holdout access.
The repository-frozen prospective plan has **not** been externally registered;
external registration and ethics approval remain gates before human research.

## Literature and access boundaries

[Woo et al. (2023), DOI 10.12779/dnd.2023.22.4.148](https://pmc.ncbi.nlm.nih.gov/articles/PMC10654483/)
report 11 analyzed patients and 13 controls and a nonsignificant temporal-window
comparison, p=0.15. This is inconclusive for a universal group deficit and cannot
establish equality. Small N and limited trials constrain precision; neither
adequate power nor a quantitative claim of inadequate power can be deduced from
p=0.15 alone without a specified effect and design. No post-hoc observed-power
argument is used. The older R2 identifier `KIM_ET_AL_2023` is historical; the
article's first author is Sung-Ho Woo.

The Teghil publication and the R3 source ledger are background, not received
individual data. [Issue #13](https://github.com/Hawkar-usls/Simptomat/issues/13)
records that the first request was **sent on 2026-11-22** and is awaiting an
external response. The old R3 draft/ledger is a frozen pre-dispatch record.
No second message is sent, and no new author outreach is authorized by R2B.
No participant-level records were requested from a tool or analyzed in this work.

## Claim ceiling and reproducibility

Run `python -m tools.temporal_awareness_r2b --audit` for deterministic results;
run `python -m tools.temporal_awareness_r2b_reproduce` to compare the checked-in
results and source-hash manifest. The dedicated R2B workflow runs R1–R3
regressions, R2B methods and power tests, repository invariants and an exact JSON
replay, then uploads the synthetic receipt.

Engineering validation and scientific validation remain separate. Passing CI
admits only reproducible offline synthetic mathematics and methods planning.
Clinical validation, mechanism attribution and independent participant-level
replication remain **HOLD**. `ALZHEIMER_DIAGNOSED`, `TIMELESS_CONSCIOUSNESS_PROVEN`,
`TIME_TRAVEL_PROVEN`, `SOLO_CONSCIOUSNESS_PROVEN` and
`PHYSICAL_TIME_CHANGED_BY_GROUP` remain forbidden promotions.

R2B introduces no clinical authority, patient ingestion, live screening,
production model update, physical intervention or automatic cross-repository
runtime action. Linking the evidence to RULE #1 does not promote RULE #1 to a
validated claim about consciousness or physical time.
