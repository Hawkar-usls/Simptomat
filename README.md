<div align="center">

# Simptomat
### Consent-first adaptive differential-diagnostic reasoning organ for JANUS

![Status](https://img.shields.io/badge/status-active_prototype-2ea44f)
![Class](https://img.shields.io/badge/class-health_information_research-6e7681)
![JANUS](https://img.shields.io/badge/JANUS-diagnostic_reasoning_organ-8250df)
![Clinical validation](https://img.shields.io/badge/clinical_validation-not_established-d73a49)

</div>

## Status

**ACTIVE_PROTOTYPE.** Simptomat is a consent-first research system for adaptive symptom screening, differential-diagnosis reasoning, disease-candidate ranking, uncertainty handling, next-question selection, confirmation-step suggestion, and longitudinal calibration from consented cases.

Simptomat **does form diagnostic hypotheses**. What it does not have is independent clinical authority to declare those hypotheses clinically confirmed. It is not a medical device, treatment system, clinician of record, or substitute for emergency/clinical evaluation.

Simptomat is now declared as the `diagnostic_reasoning` domain organ of the **JANUS federated organism** and has a typed, bidirectional integration contract with `Hawkar-usls/Demi_Head`.

## Abstract

Simptomat asks one question at a time, maintains a live differential set, and uses each answer to update which diseases or syndromes remain supported, compatible, contradicted, or unresolved. The next question should be selected for its ability to distinguish live hypotheses, unless a safety concern requires immediate real-world escalation.

The intended loop is:

```text
SCREEN
  ↓
DIFFERENTIATE
  ↓
HYPOTHESIZE
  ↓
TEST
  ↓
LEARN
```

The system may produce a ranked differential diagnosis and a lead diagnostic hypothesis, while explicitly preserving contradictory evidence and uncertainty. When conversation alone cannot resolve the differential, Simptomat should identify the next real-world measurement or clinical confirmation step that could discriminate candidates.

In parallel, participants who give separate explicit consent may contribute pseudonymized case records to the calibration archive. Those records are used to improve question wording, branching, discrimination, ranking, uncertainty handling, and later—when independent reference labels exist—measurable diagnostic performance.

## Diagnostic reasoning model

```text
D0 = broad admissible differential set

answer(Q1)
   ↓
update evidence for each candidate
   ↓
D1 = ranked live candidates + contradictions + uncertainty
   ↓
choose next question with high discriminatory value
   ↓
answer(Q2)
   ↓
...
   ↓
Dn = ranked differential diagnosis
   ↓
lead hypothesis + alternatives
   ↓
next best confirmation / measurement step
```

Until a probability model is independently calibrated, candidate ranking should use evidence states rather than invented numerical certainty:

```text
SUPPORTED
COMPATIBLE
WEAKLY_COMPATIBLE
CONTRADICTED
INSUFFICIENT_DATA
ESCALATE_FOR_REAL_WORLD_EVALUATION
```

Core contract: [`protocols/SIMPTOMAT_DIAGNOSTIC_REASONING_CORE-v1.0.json`](protocols/SIMPTOMAT_DIAGNOSTIC_REASONING_CORE-v1.0.json).

## JANUS organism integration

Simptomat participates in JANUS as a **health-domain differential-reasoning and calibration organ**, not as a global truth authority.

Membership declaration:
[`/.janus/JANUS_ORGANISM_LINK.json`](.janus/JANUS_ORGANISM_LINK.json)

DemiHead Nexus peer link:
[`/.janus/DEMIHEAD_NEXUS_LINK.json`](.janus/DEMIHEAD_NEXUS_LINK.json)

Bridge contract:
[`integrations/JANUS_DEMIHEAD_DIAGNOSTIC_BRIDGE-v1.0.json`](integrations/JANUS_DEMIHEAD_DIAGNOSTIC_BRIDGE-v1.0.json)

The typed spiral is:

```text
HUMAN SYMPTOM / QUESTION
        ↓
SIMPTOMAT
  differential update
  ranked hypotheses
  contradictions + uncertainty
        ↓ minimized typed packet
DEMIHEAD
  provenance review
  contradiction review
  claim-ceiling enforcement
        ↓ bounded epistemic review
SIMPTOMAT
  reintegrate review
        ↓
next discriminating question
        OR
next external measurement
        ↓
new state / next spiral turn
```

Simptomat can also exchange bounded artifacts with other JANUS organs through the canonical organism topology: `janus-lapis` for competing-hypothesis metabolism, `janus-io-public` for measurement receipts, `janus-meta-registry` for provenance/calibration history, and the `Janus` gateway for typed routing.

```text
DEMIHEAD_REVIEW != CLINICAL_CONFIRMATION
ROUTE != AUTHORITY
ORGAN_MEMBERSHIP != MEDICAL_AUTHORITY
CONSENT_SCOPE_MUST_SURVIVE_TRANSPORT
PRIVATE_HEALTH_DATA != PUBLIC_HABITAT_PAYLOAD
```

Raw transcripts and direct identifiers are denied by default on the Simptomat→DemiHead route. The normal inter-organ packet is a minimized reasoning summary, not the participant's raw conversation.

## Implemented scope

- adaptive one-question-at-a-time conversational screening;
- explicit differential-diagnosis reasoning contract;
- ranked diagnostic-hypothesis output model;
- support / contradiction / uncertainty tracking;
- next-best-question and next-measurement logic contract;
- machine-readable consented case format;
- pseudonymized public case archive;
- uncertainty-preserving answer normalization;
- calibration-development ledger;
- claim-ceiling and anti-self-deception rules;
- JANUS Git Habitat integration;
- JANUS organism member declaration;
- typed bidirectional DemiHead Nexus integration contract;
- first founder pilot: 33-question symptomatic prion-pattern screening;
- privacy-hardened public web client.

## First calibration case

[`cases/consented/SIM-P0001-2026-08-26-PRION.json`](cases/consented/SIM-P0001-2026-08-26-PRION.json)

The founding pilot began with a prion-disease hypothesis and repeatedly tested it against competing explanations and expected neurological features. Its terminal is:

```text
SYMPTOMATIC_PRION_PATTERN_NOT_DETECTED
```

This means the targeted symptomatic prion hypothesis was not supported by the self-reported branch strongly enough to trigger the prion escalation terminal. It does **not** prove absence of prions or exclude presymptomatic disease.

```text
DIAGNOSTIC_HYPOTHESIS != CLINICALLY_CONFIRMED_DIAGNOSIS
RANKED_FIRST != CERTAIN
PATTERN_NOT_DETECTED != DISEASE_PROVEN_ABSENT
SELF_REPORT != CLINICAL_MEASUREMENT
```

The pilot has no independent clinical reference diagnosis and therefore is **not** counted as a true negative, false negative, true positive, or false positive.

The frozen founding protocol remains unchanged for reproducibility:
[`protocols/PRION_SYMPTOMATIC_PATTERN_SCREEN-v1.0.json`](protocols/PRION_SYMPTOMATIC_PATTERN_SCREEN-v1.0.json).

## Calibration model

Simptomat learns in two distinct stages.

```text
CONSENTED SELF-REPORT CASES
        ↓
wording / branching / discrimination / ranking / uncertainty calibration
        ↓
VERSION-FROZEN PROTOCOL + MODEL
        ↓
INDEPENDENT REFERENCE-LABELED CASES
        ↓
FROZEN HOLDOUT / EXTERNAL VALIDATION
        ↓
only then: diagnostic-performance metrics
```

Repeated cases can reveal recurring symptom combinations and inefficient questions, but repeated self-report alone cannot establish sensitivity, specificity, predictive value, or clinical utility.

Current metric gate: **BLOCKED**.

See [`calibration/CALIBRATION_STATE.json`](calibration/CALIBRATION_STATE.json).

## Consent and privacy

Conversation consent, inter-organ processing, and public-case consent are distinct scopes. Public persistence requires explicit consent for that record; transport does not silently expand consent.

Public cases are minimized and pseudonymized. By default Simptomat does not publish names, exact birth dates, addresses, contact/account identifiers, relative identities, raw transcripts, medical-record identifiers, images, voice, or genetic data.

A public Git repository has persistent history and may be cloned; participants must be warned that later removal cannot guarantee erasure from every copy/cache/history.

Full policy: [`docs/CONSENT_AND_DATA_GOVERNANCE.md`](docs/CONSENT_AND_DATA_GOVERNANCE.md).

## Epistemic boundary

Simptomat inherits the JANUS global anti-self-deception constitution:

[`JANUS-GLOBAL-EPISTEMIC-SELF-DECEPTION-TRUTH-CONSTITUTION-v1.0.json`](https://github.com/Hawkar-usls/janus-meta-registry/blob/main/registry/epistemic/JANUS-GLOBAL-EPISTEMIC-SELF-DECEPTION-TRUTH-CONSTITUTION-v1.0.json)

Core laws:

```text
DIAGNOSTIC_HYPOTHESIS != CLINICALLY_CONFIRMED_DIAGNOSIS
DEMIHEAD_REVIEW != CLINICAL_CONFIRMATION
RANKING != CERTAINTY
MODEL_SCORE != CLINICAL_PROBABILITY_UNLESS_CALIBRATED
UNCERTAIN != NO
OLD_STABLE_TRAIT != NEW_PROGRESSIVE_SYMPTOM
ANECDOTAL_SELF_TEST != CLINICAL_EXAMINATION
AI_OUTPUT != MEDICAL_AUTHORITY
ONE_CASE != CALIBRATION
REPEATED_CASES != CLINICAL_VALIDATION
DEVELOPMENT_SET != HOLDOUT_SET
REGISTRY_PRESENCE != MEDICAL_TRUTH
```

Negative, null, ambiguous, contradictory, and boring/common explanations are first-class records. A favored diagnosis must remain falsifiable.

## Habitat

Repository constellation link:
[`/.janus/HABITAT_LINK.json`](.janus/HABITAT_LINK.json)

Simptomat role/contract:
[`habitat/SIMPTOMAT_HABITAT-v1.0.json`](habitat/SIMPTOMAT_HABITAT-v1.0.json)

Habitat provides repository-scale provenance and handoff only.

```text
HABITAT_LINK != COMMAND_AUTHORITY
WRITE_BACK_DEFAULT = DENY
```

## Repository map

```text
Simptomat/
├── .janus/
│   ├── HABITAT_LINK.json
│   ├── JANUS_ORGANISM_LINK.json
│   └── DEMIHEAD_NEXUS_LINK.json
├── cases/
│   └── consented/                  # explicit-consent pseudonymized records
├── calibration/
│   └── CALIBRATION_STATE.json
├── docs/
│   └── CONSENT_AND_DATA_GOVERNANCE.md
├── habitat/
│   └── SIMPTOMAT_HABITAT-v1.0.json
├── integrations/
│   └── JANUS_DEMIHEAD_DIAGNOSTIC_BRIDGE-v1.0.json
├── protocols/
│   ├── SIMPTOMAT_DIAGNOSTIC_REASONING_CORE-v1.0.json
│   └── PRION_SYMPTOMATIC_PATTERN_SCREEN-v1.0.json
├── schemas/
│   └── simptomat-screening-case.v1.schema.json
├── PROJECT_STATUS.json
├── index.html
└── README.md
```

## Reviewer path

1. Read [`PROJECT_STATUS.json`](PROJECT_STATUS.json).
2. Read the diagnostic-reasoning core contract.
3. Read the JANUS/DemiHead bridge contract.
4. Inspect [`docs/CONSENT_AND_DATA_GOVERNANCE.md`](docs/CONSENT_AND_DATA_GOVERNANCE.md).
5. Inspect the case schema and founding pilot.
6. Check [`calibration/CALIBRATION_STATE.json`](calibration/CALIBRATION_STATE.json) before interpreting any performance claim.

## Current non-claims

```text
CLINICAL_VALIDATION = NOT_ESTABLISHED
DIAGNOSTIC_ACCURACY = NOT_ESTABLISHED
SENSITIVITY = NOT_ESTABLISHED
SPECIFICITY = NOT_ESTABLISHED
CLINICAL_DIAGNOSTIC_AUTHORITY = FALSE
TREATMENT_AUTHORITY = FALSE
EMERGENCY_TRIAGE_SUBSTITUTE = FALSE
MEDICAL_DEVICE_STATUS = NOT_CLAIMED
PRODUCTION_CROSS_REPO_RUNTIME = NOT_ESTABLISHED
```

These boundaries do **not** prohibit Simptomat from performing diagnostic reasoning or ranking disease hypotheses; they prevent an internally generated hypothesis or a DemiHead review from being misrepresented as externally confirmed medical fact.

## Presentation

Repository presentation follows the account-wide [Public Repository Presentation Standard](https://github.com/Hawkar-usls/Janus/blob/main/docs/PUBLIC_REPOSITORY_PRESENTATION_STANDARD.md).

No institutional affiliation or endorsement is implied.

## TACHYON R1 — Time awareness, event sequence, and memory (synthetic research)

**Bounded synthetic-only research, not medical screening.** The [research protocol](research/temporal_awareness/SIMPTOMAT_TACHYON_ALZHEIMER_R1_2026-11-22.json) uses published Alzheimer's/dementia temporal-awareness literature to distinguish **observable online engagement**, **immediate item recognition**, **event-order judgments** and **delayed recall**, with optional subjective felt passage of time.

This is a supplementary research and falsification lane linked read-only to [JANUS RULE #1](https://github.com/Hawkar-usls/janus-meta-registry/blob/7ce207fab7b5d337cb549a326c6cd71fdc5b8340/data/JANUS-RULE-001-FIRST-PERSON-TEMPORAL-CONSTRUCTION-2026-11-22-v1.0.json). A person might remain behaviorally engaged while delayed recall or temporal ordering differs; neither behavioral engagement nor absent temporal-feeling alone proves timeless consciousness. Alzheimer's is a disease, not a mechanism for time travel.

The [Python reference](tools/temporal_awareness_lab.py) accepts *only declared synthetic fixtures*, never real people or medical records, and runs seven differential demonstration cases with the --demo switch. The [research bridge](integrations/JANUS_TACHYON_TEMPORAL_AWARENESS_RESEARCH_BRIDGE-v1.0.json) is read-only, does not enable ambient/cross-repo transport and has zero medical authority. The [CI workflow](.github/workflows/tachyon-temporal-awareness-r1.yml) checks existing consented-case invariants, adversarial synthetic tests and all seven demo profiles.

No patient observations, clinical labels, new neural training, human stimulation, validated dementia classifier, prospective time-travel evidence or production service activation is claimed. Any human study requires separate ethics/clinician review, explicit consent, private storage, clinical reference standards and independent validation.

## TACHYON R2 — Identifiability and full-grid temporal-awareness audit

The [R2 research protocol](research/temporal_awareness/SIMPTOMAT_TACHYON_R2_IDENTIFIABILITY_2026-11-22.json) extends R1 with a complete **1,296-vector synthetic (0..5)^4 audit** of observable engagement, immediate recognition, temporal-order task performance and delayed recall. It reports one-response fragility and a fundamental causal identifiability limitation: **the same four observable task counts can arise from different underlying mechanisms**. The R1 labels are descriptive toy patterns, not clinically calibrated causes.

The R2 analyzer runs in GitHub Actions using `python -m tools.temporal_awareness_r2 --audit`. [R2 CI](.github/workflows/tachyon-temporal-awareness-r2.yml) executes the existing R1 synthetic/privacy tests, 16 R2 tests, full enumeration and fail-closed checks. The published preliminary MCI/AD study's p=0.15 is a negative control against a blanket claim of a significant between-group perceptual deficit; its report is **not** independent replication, equivalence proof or access to patient-level data. Teghil et al. 2023 report that individual-level data are available by reasonable request; no permission or data have been received here.

R2 is a bounded **methods-only synthetic CI** study. No Alzheimer diagnosis, no patient records, no live screening, no assessment of consciousness, no pharmacological intervention or capsule control, no model updates and no claim of time travel. Human research remains HOLD pending ethical approval, consent, independent measurement and an externally preserved test set.

## TACHYON R3 — Independent data scouting and scientific eligibility

The [R3 dataset qualification registry](research/temporal_awareness/SIMPTOMAT_TACHYON_R3_INDEPENDENT_DATA_SCOUT_2026-11-22.json) inventories six independently published sources that might help falsify the JANUS RULE #1 research hypothesis. It explicitly separates **time-locked observable engagement**, **immediate recognition**, **direct event-order perception**, and **delayed same-item memory**, and distinguishes each from published task descriptions or indirect proxies.

The [R3 readiness auditor](tools/temporal_awareness_r3_source_audit.py) processes *only publication metadata* from the checked-in JSON (no medical records or patient measurements). Its result is deliberately **HOLD_NO_QUALIFIED_PARTICIPANT_LEVEL_INDEPENDENT_DATA** while source access, individual rows, matched tasks and documented rights are unavailable. A paper's statement that data are available upon request or a landing page linking OSF does not prove that we have downloaded or inspected the original data.

Sources include Teghil et al. 2023 (mixed timing, memory, attention, but data only by author request), Hampstead et al. 2014 (order + immediate/delayed memory, file accessibility unverified), Payne et al. 2023 (open OSF data declared, elderly controls rather than AD cases; event segmentation, recognition and order tasks), Seattle–Groningen 2026 (public OSF data declared, longitudinal MCI/controls memory, direct order task not verified), UCL dementia subjective-time research (patient data on request), and a 2026 Zenodo aging dataset with **restricted files**. No data have been accessed or copied to GitHub.

The [request draft](docs/TACHYON_R3_TEGHIL_DATA_REQUEST_DRAFT.md) and source ledger preserve the pre-dispatch state. **The first request was sent on 2026-11-22; [Issue #13](https://github.com/Hawkar-usls/Simptomat/issues/13) records `AWAITING_EXTERNAL_RESPONSE`.** No follow-up is sent by this research lane. The [R3 GitHub Actions workflow](.github/workflows/tachyon-temporal-awareness-r3.yml) preserves the R1+R2 tests, runs source-manifest tests, checks the no-data/no-diagnosis gates and publishes only a source-readiness JSON receipt.

## TACHYON R2B — Independent methods review

The [R2B review response](docs/TACHYON_R2B_INDEPENDENT_METHODS_REVIEW.md) corrects the external review: 1296 vectors comprise **48 candidates + 1232 indeterminate + 16 NO_DEMO_DISSOCIATION**, so 1248 are noncandidates. The historical 36 R1/R2 checks are software unit tests, not clinical hypotheses.

The [offline audit](tools/temporal_awareness_r2b.py) reproduces R1, compares the 704/8640 directed-edge flips with constant, one-feature and seeded randomized controls, sweeps every admissible integer LOW/HIGH pair, and constructs an explicit many-to-one latent forward map with identical observation distributions. Flip rates describe synthetic classifier geometry; they do not establish mechanisms or diagnostic accuracy. No oracle ceiling is available.

The [prospective study plan](docs/TACHYON_R2B_PREREGISTRATION.md) specifies paired primary endpoints, a confirmatory multiplicity family, independent participant holdout, ethics/consent and source/safety gates. Its [power calculator](tools/temporal_awareness_r2b_power.py) states effect and recruitment assumptions; 48/1296 is **not clinical prevalence**. The plan is repository-frozen and **pending external registration**, with no real participant data analyzed.

[Checked-in machine-readable results](research/temporal_awareness/SIMPTOMAT_TACHYON_R2B_RESULTS_2026-11-22.json) are replayed exactly by `python -m tools.temporal_awareness_r2b_reproduce`; [R2B Actions](.github/workflows/tachyon-temporal-awareness-r2b.yml) checks source hashes, regressions and scientific boundaries. Engineering checks can pass while scientific/clinical validation remains **HOLD**. Production models, live screening and patient-data routes receive no new authority.

The next gate is a privacy-compliant individual-level dataset with all four same-participant task variables, independent provenance and documented matching of stimulus timing; then preregistration, scientific review and heldout analysis. **Clinical efficacy, Alzheimer's diagnosis, subjective timelessness and physical time travel remain unestablished.**
