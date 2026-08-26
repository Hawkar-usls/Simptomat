# Simptomat Case Archive

This directory is the consent-gated public research archive for normalized Simptomat screening and diagnostic-reasoning records.

## Layout

```text
cases/
├── README.md
└── consented/
    └── SIM-P0001-2026-08-26-PRION.json
```

Future records use the naming convention:

```text
SIM-P####-YYYY-MM-DD-<SCREENING_DOMAIN>.json
```

## Admission gate

A case enters `consented/` only when all of the following are true:

1. the participant explicitly consents to a public pseudonymized record;
2. the participant is an adult, unless a separate approved minor/guardian process exists;
3. direct identifiers and unnecessary sensitive details are removed;
4. the raw conversation is not published by default;
5. uncertainty is preserved rather than coerced into `YES` or `NO`;
6. the record declares whether any independent clinical reference label exists;
7. diagnostic hypotheses, if present, are labeled research hypotheses rather than clinically confirmed diagnoses;
8. the participant is warned that public Git history cannot guarantee complete later erasure.

See [`../docs/CONSENT_AND_DATA_GOVERNANCE.md`](../docs/CONSENT_AND_DATA_GOVERNANCE.md).

## What a case may contain

A case can preserve both the questioning path and the diagnostic reasoning produced from it:

```text
QUESTION / ANSWER PATH
        ↓
DERIVED FEATURES
        ↓
RANKED DIFFERENTIAL DIAGNOSIS
        ↓
LEAD DIAGNOSTIC HYPOTHESIS + ALTERNATIVES
        ↓
SUPPORT / CONTRADICTIONS / UNCERTAINTY
        ↓
NEXT BEST CONFIRMATION STEP
```

These fields are allowed under the project claim ceiling. They do not become clinical ground truth merely because they are stored in the archive.

```text
DIAGNOSTIC_HYPOTHESIS != CLINICALLY_CONFIRMED_DIAGNOSIS
RANKING != CERTAINTY
SELF_REPORT_CASE != REFERENCE_STANDARD
```

## Calibration classes

```text
FOUNDING_PILOT_CASE
DEVELOPMENT_CASE
FROZEN_HOLDOUT_CASE
EXTERNAL_VALIDATION_CASE
WITHDRAWN_CASE
```

A case can be useful without being a diagnostic ground truth.

```text
SELF_REPORT_CASE != TRUE_NEGATIVE_OR_TRUE_POSITIVE
MANY_CASES != CLINICAL_VALIDATION
```

## First record

`SIM-P0001-2026-08-26-PRION.json` is the founding pilot. It contains 33 normalized adaptive questions from a self-reported screening conversation. Its terminal is:

```text
SYMPTOMATIC_PRION_PATTERN_NOT_DETECTED
```

That terminal means only that the reported answers did not assemble the targeted rapidly progressive symptomatic pattern strongly enough to support the prion hypothesis in that branch. It does **not** mean `PRION_ABSENT` and does not establish a clinically confirmed diagnosis.

The first record is intentionally preserved in its founding format. Future records may additionally use the differential-diagnosis fields defined by the case schema and `protocols/SIMPTOMAT_DIAGNOSTIC_REASONING_CORE-v1.0.json`.
