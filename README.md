<div align="center">

# Simptomat
### Consent-first conversational symptom-pattern screening research prototype

![Status](https://img.shields.io/badge/status-active_prototype-2ea44f)
![Class](https://img.shields.io/badge/class-health_information_research-6e7681)
![Clinical validation](https://img.shields.io/badge/clinical_validation-not_established-d73a49)

</div>

## Status

**ACTIVE_PROTOTYPE.** Simptomat is being developed as a consent-first research system for adaptive conversational symptom-pattern screening, uncertainty handling, branching-logic calibration, and false-positive resistance.

It is **not** a medical device, diagnostic service, treatment system, or substitute for emergency/clinical evaluation.

## Abstract

Simptomat asks one question at a time, updates the next question from the preceding answer, and preserves uncertainty instead of forcing a binary diagnosis. The research objective is to learn which question sequences are useful for distinguishing symptom patterns while keeping claim ceilings explicit.

The public calibration archive contains only pseudonymized records from participants who explicitly consent to publication.

## Implemented scope

- adaptive one-question-at-a-time conversational screening;
- machine-readable consented case format;
- pseudonymized public case archive;
- uncertainty-preserving answer normalization;
- calibration-development ledger;
- claim-ceiling and anti-self-deception rules;
- JANUS Git Habitat integration;
- first founder pilot: 33-question symptomatic prion-pattern screening;
- privacy-hardened public-web-client workstream.

## First calibration case

[`cases/consented/SIM-P0001-2026-08-26-PRION.json`](cases/consented/SIM-P0001-2026-08-26-PRION.json)

The founding pilot terminal is:

```text
SYMPTOMATIC_PRION_PATTERN_NOT_DETECTED
```

This means only that the self-reported answers did not assemble the targeted rapidly progressive symptomatic pattern.

```text
PATTERN_NOT_DETECTED != DISEASE_PROVEN_ABSENT
SCREENING_PATTERN != DIAGNOSIS
SELF_REPORT != CLINICAL_MEASUREMENT
```

The pilot has no independent clinical reference diagnosis and therefore is **not** counted as a true negative, false negative, true positive, or false positive.

## Calibration model

Simptomat separates development from validation.

```text
SELF-REPORT CASES
        ↓
wording / branching / uncertainty calibration
        ↓
VERSION-FROZEN PROTOCOL
        ↓
INDEPENDENT REFERENCE-LABELED CASES
        ↓
FROZEN HOLDOUT / EXTERNAL VALIDATION
        ↓
only then: diagnostic-performance metrics
```

Current metric gate: **BLOCKED**.

See [`calibration/CALIBRATION_STATE.json`](calibration/CALIBRATION_STATE.json).

## Consent and privacy

No participant record is persisted without explicit consent for that record.

Public cases are minimized and pseudonymized. By default Simptomat does not publish names, exact birth dates, addresses, contact/account identifiers, relative identities, raw transcripts, medical-record identifiers, images, voice, or genetic data.

A public Git repository has persistent history and may be cloned; participants must be warned that later removal cannot guarantee erasure from every copy/cache/history.

Full policy: [`docs/CONSENT_AND_DATA_GOVERNANCE.md`](docs/CONSENT_AND_DATA_GOVERNANCE.md).

## Epistemic boundary

Simptomat inherits the JANUS global anti-self-deception constitution:

[`JANUS-GLOBAL-EPISTEMIC-SELF-DECEPTION-TRUTH-CONSTITUTION-v1.0.json`](https://github.com/Hawkar-usls/janus-meta-registry/blob/main/registry/epistemic/JANUS-GLOBAL-EPISTEMIC-SELF-DECEPTION-TRUTH-CONSTITUTION-v1.0.json)

Core laws:

```text
UNCERTAIN != NO
OLD_STABLE_TRAIT != NEW_PROGRESSIVE_SYMPTOM
ANECDOTAL_SELF_TEST != CLINICAL_EXAMINATION
AI_OUTPUT != MEDICAL_AUTHORITY
ONE_CASE != CALIBRATION
REPEATED_CASES != CLINICAL_VALIDATION
DEVELOPMENT_SET != HOLDOUT_SET
REGISTRY_PRESENCE != MEDICAL_TRUTH
```

Negative, null, ambiguous, and contradictory cases are first-class records.

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
├── schemas/
│   └── simptomat-screening-case.v1.schema.json
├── PROJECT_STATUS.json
├── index.html
└── README.md
```

## Reviewer path

1. Read [`PROJECT_STATUS.json`](PROJECT_STATUS.json).
2. Inspect [`docs/CONSENT_AND_DATA_GOVERNANCE.md`](docs/CONSENT_AND_DATA_GOVERNANCE.md).
3. Inspect the case schema.
4. Inspect the founding pilot record.
5. Check [`calibration/CALIBRATION_STATE.json`](calibration/CALIBRATION_STATE.json) before interpreting any result.

## Current non-claims

```text
CLINICAL_VALIDATION = NOT_ESTABLISHED
DIAGNOSTIC_ACCURACY = NOT_ESTABLISHED
SENSITIVITY = NOT_ESTABLISHED
SPECIFICITY = NOT_ESTABLISHED
DIAGNOSTIC_AUTHORITY = FALSE
TREATMENT_AUTHORITY = FALSE
EMERGENCY_TRIAGE_SUBSTITUTE = FALSE
MEDICAL_DEVICE_STATUS = NOT_CLAIMED
```

## Presentation

Repository presentation follows the account-wide [Public Repository Presentation Standard](https://github.com/Hawkar-usls/Janus/blob/main/docs/PUBLIC_REPOSITORY_PRESENTATION_STANDARD.md).

No institutional affiliation or endorsement is implied.
