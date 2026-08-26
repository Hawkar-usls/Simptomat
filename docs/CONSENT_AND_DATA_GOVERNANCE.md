# Simptomat — Consent & Data Governance

Simptomat is an **active research prototype for conversational symptom screening and adaptive differential-diagnostic reasoning**. It may form and rank diagnostic hypotheses. It is not a medical device, clinician of record, treatment system, or emergency-triage substitute, and its hypotheses are not automatically clinically confirmed diagnoses.

## Core rule

```text
NO EXPLICIT CONSENT -> NO CASE RECORD
SELF-REPORT != CLINICAL LABEL
DIAGNOSTIC_HYPOTHESIS != CLINICALLY_CONFIRMED_DIAGNOSIS
RANKING != CERTAINTY
REPEATED CASES != CLINICAL VALIDATION
PUBLIC REPOSITORY != PERMISSION FOR UNBOUNDED REUSE
```

## What may be stored publicly

Only a deliberately minimized, pseudonymized record may enter `cases/consented/`.

Allowed by default:

- random/public subject identifier (`SIM-P####`);
- broad age band when relevant;
- normalized answers required for the screening protocol;
- uncertainty labels;
- protocol/version identifiers;
- non-identifying exposure categories;
- screening terminal and claim ceiling;
- ranked research diagnostic hypotheses when produced;
- non-identifying supporting/contradicting features and unresolved alternatives;
- suggested next confirmation step when relevant;
- provenance describing how the record was produced.

Not allowed by default:

- real names;
- exact birth dates;
- street addresses or precise geolocation;
- phone numbers, emails, account identifiers, Telegram IDs, or other contact handles;
- raw chat transcripts;
- names/identifiers of relatives;
- photos, voice samples, documents, medical-record numbers, or genetic data;
- details not needed for the declared research question.

## Consent contract

Consent must be explicit for **each participant and each public record**. Consent from one participant cannot be inherited by another person. Participation, reading the repository, following a link, or answering a question does not by itself authorize publication.

Consent to use the conversational interface is separate from consent to publish a pseudonymized case. A client session may therefore operate with public-case persistence disabled.

The participant must understand that the repository is public and Git is historically persistent: removing a current file cannot guarantee deletion from forks, caches, clones, or prior Git objects.

A participant may request that the current public record be removed and that future use stop. Simptomat must preserve a non-identifying tombstone stating that the record was withdrawn, unless the participant asks for no public tombstone and doing so is technically/legalistically possible.

## Adults by default

The public calibration lane is for consenting adults by default. Records involving minors require a separate, explicitly designed ethics/guardian process and must not be added merely by extending this template.

## Diagnostic reasoning vs clinical confirmation

Simptomat is allowed to do the research analogue of differential diagnosis:

```text
symptoms / history
    ↓
maintain competing disease hypotheses
    ↓
ask discriminating questions
    ↓
rank candidates
    ↓
identify support / contradictions / uncertainty
    ↓
suggest the next useful confirmation or measurement step
```

The claim ceiling is applied **after** reasoning, not by forbidding reasoning itself.

```text
SIMPTOMAT_MAY_FORM_DIAGNOSTIC_HYPOTHESES = TRUE
SIMPTOMAT_MAY_RANK_DISEASE_CANDIDATES = TRUE
SIMPTOMAT_MAY_SUGGEST_CONFIRMATION_STEPS = TRUE

DIAGNOSTIC_HYPOTHESIS != CLINICALLY_CONFIRMED_DIAGNOSIS
MODEL_SCORE != CLINICAL_PROBABILITY_UNLESS_CALIBRATED
SUGGESTED_TEST != MEDICAL_ORDER
```

## Calibration hierarchy

Each case must declare its label source.

```text
SELF_REPORT_ONLY
    < CLINICIAN_REPORTED_WITH_CONSENT
    < INDEPENDENT_REFERENCE_STANDARD
```

This ordering is about evidence strength, not about the worth of the participant.

Self-reported cases can improve wording, branching, ambiguity handling, candidate discrimination, ranking behavior, next-question selection, and false-positive resistance. They **cannot** by themselves establish sensitivity, specificity, predictive value, clinical utility, or diagnostic accuracy.

Performance calibration requires an appropriate study design and independently established reference labels. Development cases and evaluation/holdout cases must be separated before accuracy claims are made.

## Anti-self-deception gate

Every case inherits the JANUS epistemic constitution:

`JANUS-GLOBAL-EPISTEMIC-SELF-DECEPTION-TRUTH-CONSTITUTION-v1.0.json`

Simptomat-specific invariants:

```text
UNCERTAIN != NO
OLD STABLE TRAIT != NEW PROGRESSIVE SYMPTOM
ANECDOTAL SELF-TEST != NEUROLOGICAL EXAMINATION
MODEL CONFIDENCE != CLINICAL PROBABILITY
RANKED FIRST != CERTAIN
PATTERN ABSENT != DISEASE ABSENT
PATTERN PRESENT != DISEASE PRESENT
ONE CASE != POPULATION
MANY SIMILAR CASES != CAUSATION
```

Negative, uncertain, contradictory, and incomplete cases are retained. The system must not keep only cases that make its branching logic or preferred diagnosis look successful.

A favored diagnostic hypothesis must remain falsifiable. Questions or measurements capable of weakening it should be preferred over questions that merely accumulate confirming detail.

## Safety escalation

If a conversation contains a potentially urgent medical situation, the research/calibration objective is subordinate to safety. Simptomat should stop ordinary branching and recommend appropriate real-world medical evaluation. It must not attempt to replace emergency services.

The exact escalation logic is protocol-specific and must be conservative. A research result or diagnostic hypothesis must never be presented as permission to delay necessary care.

## Data use and secondary research

A public case may be used only inside the consent scope recorded in that case. A new use that materially changes the purpose, exposure, or risk should obtain fresh consent where feasible.

No participant case grants Simptomat authority over the participant. No case authorizes contact, monitoring, treatment, behavioral intervention, or external action.

## Security

The public web client must not transmit raw Telegram/user identifiers by default. Session identifiers should be random and non-identifying. API endpoints should be configured explicitly; no temporary tunnel URL should be treated as a trusted production backend.

Backend responses must be rendered as untrusted content. A remote model/backend must not be allowed to inject arbitrary HTML into the client.

## Founder pilot

`SIM-P0001-2026-08-26-PRION` is the first consented public pilot record. Its role is **branching, hypothesis-falsification, and data-governance calibration**. It has no independent clinical reference diagnosis and therefore must not be counted as a true negative, false negative, true positive, or false positive.

The frozen founding protocol remains historical provenance. The project-wide diagnostic reasoning semantics are defined by `protocols/SIMPTOMAT_DIAGNOSTIC_REASONING_CORE-v1.0.json`.
