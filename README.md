<div align="center">

# Simptomat
### Consent-first adaptive differential-diagnostic reasoning research prototype

![Status](https://img.shields.io/badge/status-active_prototype-2ea44f)
![Class](https://img.shields.io/badge/class-health_information_research-6e7681)
![Clinical validation](https://img.shields.io/badge/clinical_validation-not_established-d73a49)

</div>

## Status

**ACTIVE_PROTOTYPE.** Simptomat is being developed as a consent-first research system for adaptive symptom screening, differential-diagnosis reasoning, disease-candidate ranking, uncertainty handling, next-question selection, confirmation-step suggestion, and longitudinal calibration from consented cases.

Simptomat **does form diagnostic hypotheses**. What it does not have is independent clinical authority to declare those hypotheses clinically confirmed. It is not a medical device, treatment system, clinician of record, or substitute for emergency/clinical evaluation.

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

Conversation consent and public-case consent are separate gates. No participant record is persisted in the public archive without explicit consent for that record.

Public cases are minimized and pseudonymized. By default Simptomat does not publish names, exact birth dates, addresses, contact/account identifiers, relative identities, raw transcripts, medical-record identifiers, images, voice, or genetic data.

A public Git repository has persistent history and may be cloned; participants must be warned that later removal cannot guarantee erasure from every copy/cache/history.

Full policy: [`docs/CONSENT_AND_DATA_GOVERNANCE.md`](docs/CONSENT_AND_DATA_GOVERNANCE.md).

## Epistemic boundary

Simptomat inherits the JANUS global anti-self-deception constitution:

[`JANUS-GLOBAL-EPISTEMIC-SELF-DECEPTION-TRUTH-CONSTITUTION-v1.0.json`](https://github.com/Hawkar-usls/janus-meta-registry/blob/main/registry/epistemic/JANUS-GLOBAL-EPISTEMIC-SELF-DECEPTION-TRUTH-CONSTITUTION-v1.0.json)

Core laws:

```text
DIAGNOSTIC_HYPOTHESIS != CLINICALLY_CONFIRMED_DIAGNOSIS
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
├── .janus/HABITAT_LINK.json
├── cases/
│   └── consented/                  # explicit-consent pseudonymized records
├── calibration/
│   └── CALIBRATION_STATE.json      # what may/may not currently be claimed
├── docs/
│   └── CONSENT_AND_DATA_GOVERNANCE.md
├── habitat/
│   └── SIMPTOMAT_HABITAT-v1.0.json
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
3. Inspect [`docs/CONSENT_AND_DATA_GOVERNANCE.md`](docs/CONSENT_AND_DATA_GOVERNANCE.md).
4. Inspect the case schema and founding pilot.
5. Check [`calibration/CALIBRATION_STATE.json`](calibration/CALIBRATION_STATE.json) before interpreting any performance claim.

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
```

These boundaries do **not** prohibit Simptomat from performing diagnostic reasoning or ranking disease hypotheses; they prevent an internally generated hypothesis from being misrepresented as externally confirmed medical fact.

## Presentation

Repository presentation follows the account-wide [Public Repository Presentation Standard](https://github.com/Hawkar-usls/Janus/blob/main/docs/PUBLIC_REPOSITORY_PRESENTATION_STANDARD.md).

No institutional affiliation or endorsement is implied.
