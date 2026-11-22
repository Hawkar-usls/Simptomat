# TACHYON × Simptomat R2B: prospective independent study plan

Frozen research plan, 2026-11-22. Status: **PROSPECTIVE_PLAN_PENDING_EXTERNAL_REGISTRATION**.
This repository commit timestamps a prospective plan. It is not a completed OSF/registry
registration, ethics approval, recruitment authorization, or an independent empirical
replication. R1/R2 synthetic results and the external review were already known.
R2B cannot be retroactively preregistered. The future participant study can be.
The machine-readable companion is
`research/temporal_awareness/SIMPTOMAT_TACHYON_R2B_PREREGISTRATION_2026-11-22.json`.

## Research question and population

Can independently measured event-order performance and delayed episodic recall show
different patterns relative to immediate recognition when behavioral engagement is
adequate? Neither engagement nor any task score establishes phenomenal consciousness,
subjective timelessness, disease identity, neural mechanism, or altered physical time.
RULE #1 is a user-designated research hypothesis, not a clinical reference standard.

The proposed population is consenting adults in a legally obtained, independently
collected source with documented age, language, sensory and medication context.
The initial analysis pools eligible participants; diagnosis-group contrasts are
exploratory and cannot become primary after seeing outcomes. Recruitment/source
inclusion must not depend on temporal-order or delayed-recall scores. Eligibility
uses separate protocol-compliance, engagement, and immediate-recognition checks with
cutoffs fixed from external norms in a source-specific supplement before outcome access.
The estimand applies to that eligible population, not all patients or all people with AD.
Selection on recognition can itself enrich positive recognition-minus-target differences.
External reference calibration must therefore apply the identical engagement/recognition
eligibility rule; independent gate trials remove shared trial noise but do not, by
themselves, remove this selection effect.

Every person must have independent behavioral engagement, immediate recognition,
direct experienced-event order, and delayed recall linked to the same event episodes.
Recall of calendar facts, interval estimation, and self-reported duration cannot replace
direct order perception. Timestamps, order-task retention interval, delayed-recall delay,
and task order/counterbalancing must be documented. If perception and retention cannot
be separated by the design, the order measure must be called order-task performance;
an encoding/perception mechanism remains unidentified. Subjective report and external
clock measurements remain separate optional descriptive evidence kinds.

## Two co-primary endpoints and confirmatory analysis

Validated task instruments and independent, fixed age/language-appropriate normative
transformations must be named before access. Higher normative Z means better performance.
Each participant contributes one predeclared aggregate score per task, averaging the
fixed parallel blocks. R1's five-trial HIGH/LOW counts are not clinical cutoffs and will
not define these endpoints. Normative calibration uncertainty must be quantified;
this power calculation assumes norms can be treated as fixed. If that assumption is
untenable, the final design must be amended and powered before any outcome access.

1. **Order mismatch:** `D_order = Z_immediate_recognition − Z_temporal_order − b_order`.
2. **Delayed-recall mismatch:** `D_recall = Z_immediate_recognition − Z_delayed_recall − b_recall`.

Here `b_order` and `b_recall` are expected contrasts from an independent external
reference population under the **identical eligibility rule**, optionally indexed by
fixed age/language strata. Their source, uncertainty and fixed values/functions are
locked before outcome access. They may be zero only if eligible-reference calibration
justifies zero. Norming each task on an unselected population alone is insufficient.
The present power model treats these offsets as known fixed design constants; if
calibration uncertainty matters, redesign and propagate it before outcome access.
Without a suitable eligible external reference, primary confirmatory inference is HOLD.

The two nulls are `E[D_order]=0` and `E[D_recall]=0` in the independent holdout eligible
population. The planned tests are two-sided one-sample Student t tests on the
participant differences, using all eligible complete pairs for each endpoint.
Positive estimates are the prespecified direction of target weakness relative to
immediate recognition beyond the eligible-reference expectation; negative significant estimates contradict that directional
interpretation. These tests detect task mismatch, not selective dissociation or a
diagnosis. Fixed task norms are essential because tasks may differ in ordinary difficulty.
Report means, SDs, paired `d_z`, uncertainty, raw and adjusted p values, and both
Bonferroni 97.5% confidence intervals regardless of significance.

The **only confirmatory family is these two clinically motivated research hypotheses**:
Holm step-down FWER .05 (smaller p against .025, remaining p against .05 after rejection).
The 36 historical unit tests are software checks, not statistical hypotheses. Enumerated
synthetic threshold variants and random-control seeds also do not create clinical
confirmatory tests. Additional group/endpoint claims require an amended family and
new power plan before outcome access; they cannot be silently added to this family.

No interim efficacy/futility testing or outcome-dependent recruitment is planned.
The t-model assumes independent participants and approximately normal participant
differences. Predeclared participant bootstrap intervals and robust descriptive
summaries will be sensitivity analyses, not a rule for switching to whichever test
is significant. If severe instrument or model failure is discovered, report the
failure and treat inference as exploratory under a dated amendment.

## What could confirm a selective research profile

An aggregate mismatch alone does not show specificity, equivalence, or intact capacity.
An individual descriptive sequence-specific profile requires adequate independent
engagement and recognition, weak order performance, and retained delayed recall on
both a first and a separate repeat assessment using fixed parallel forms. The
delayed-recall-specific profile reverses the two target tasks. Mixed deficits stay
mixed. No individual is selected into the primary analysis because of these patterns.

Before any outcome access, freeze instrument-specific uncertainty and reliability rules.
The provisional **research-only** profile rule on external norm scales is: recognition
and the non-target score each have lower 95% measurement interval above `Z=−0.5`,
the target's upper 95% measurement interval is below `Z=−1.5`, and the target-to-nontarget
gap exceeds 1 Z unit at both assessments. Intervals require validated individual-score
measurement error and normative uncertainty; five Bernoulli trials are inadequate.
These illustrative margins have no clinical validation and must receive psychometric
review and a source-specific frozen justification before application. Failure of that
gate means **no individual profile confirmation**, rather than a relaxed cutoff.

Profile counts, repeat agreement, and intervals are exploratory descriptive secondary
outcomes. They have no claimed familywise confirmatory interpretation and this power
analysis does not power individual profile confirmation, preserved-capacity equivalence,
subgroup discovery, or prevalence estimation. A nonsignificant difference is never
accepted as evidence of preservation or equivalence. The 16 sequence, 16 recall, and
16 mixed synthetic candidate vectors are configurations, not 48 people or hypotheses.

## Holdout, competing models, and leakage prevention

Before outcome access, an independent custodian freezes the source version/checksum,
eligibility rules, instruments, norms, analysis script, randomization seed, split
manifest, stopping rule, and this plan's version in a public registration with a
private access-controlled manifest. No individual identifiers or data enter GitHub.
Allocate people (and all their visits/trials) to development 60% or holdout 40%,
stratified by site and independently known sampling strata. Relatives/linked records
must remain in one split; if recruitment is clustered, the present independent-person
power model is invalid and redesign is required before access. An already published
summary cannot count as a previously unseen individual-level holdout outcome.

The holdout remains inaccessible to model developers until the complete analysis is
locked. Transformations based on development data never use holdout means, variances,
missingness patterns, cutoffs, or model selection. Once unlocked, run the frozen analysis
once and publish all failures/deviations. No pooling of development with holdout to
rescue an unsuccessful primary result. A second cohort is required for independent
empirical replication; a second program in the same repository is not such replication.

A secondary methods comparison contrasts these predeclared Gaussian measurement models
when the source contains **at least three independent parallel-block indicators for
each of recognition, order, and delayed recall**:

- **M_shared:** one common encoding/memory factor loads on the nine indicators;
  block intercepts, positive anchor loading, unit factor variance, and diagonal
  positive residual variances fix its scale/sign and measurement assumptions.
- **M_separable:** the same common factor plus an orthogonal order-specific factor
  on the three order indicators and an orthogonal recall-specific factor on the three
  delayed-recall indicators. All cross-loadings are fixed to zero; each factor has
  unit variance and a positive anchor. Engagement, prespecified age, sensory/language,
  medication and task-order covariates enter the same fixed regression structure in
  both models. Common-factor indicators from recognition anchor the shared factor.

Before real data access, synthetic model recovery, numerical Jacobian/rank checks and
parameter-recovery tests must show that the chosen implementation and indicator design
are identified under their stated constraints. Before holdout unlock, fit parameters
only on development data, freeze optimizer, seed/restarts, convergence criteria,
regularization and all predictive procedures. Failure of identification, convergence,
normality/reliability or indicator coverage blocks this comparison. It does not license
substituting an unconstrained factor model after observing holdout outcomes.

Evaluate participant-wise conditional predictive log likelihood of the six order/recall
indicators given recognition indicators and frozen covariates, together with calibration
and residual checks. Report paired log-score differences and participant-bootstrap
intervals as secondary methods estimates, without a confirmatory clinical p-value.
Improved prediction supports only the tested measurement model's usefulness; it does
not identify a unique neural mechanism or prove that latent factors exist biologically.

## Applied power and feasibility

`python -m tools.temporal_awareness_r2b_power --audit` evaluates fixed hypothetical
assumptions offline. It integrates the noncentral paired-t model, with `df=n−1` and
noncentrality `d_z√n`; no normal-approximation sample size or patient prevalence is used.
Here `d_z=E[D]/SD(D)` uses the SD of **participant paired differences**. Trial counts
do not multiply the independent N. The two tests use conservative two-sided alpha .025
for planning. Correlation between endpoints is not assumed: at least 90% marginal power
for each yields at least 80% probability of both rejections by the union bound when both
assumed alternatives hold. This is not 90% joint power.

| Hypothetical paired d_z | Marginal power | Evaluable holdout people | Total evaluable at 40% holdout | Expected recruits at 20% attrition |
|---|---:|---:|---:|---:|
| .20 | .80 | 241 | 603 | 754 |
| .20 | .90 | 313 | 783 | 979 |
| .30 | .80 | 109 | 273 | 342 |
| .30 | .90 | 141 | 353 | 442 |
| .50 | .80 | 41 | 103 | 129 |
| .50 | .90 | 53 | 133 | 167 |

The illustrative .30/.90 design assumes a .30 reference-centered normative-score mean mismatch with SD(D)=1
for each endpoint. Neither parameter has been estimated. For equal task SD `s` and
within-person task correlation `rho`, `SD(D)=s√[2(1−rho)]`; reliability, correlation,
site/family clustering and missingness can materially change N. Separate reliability
and cluster simulations are required before a real design with such features is approved.
Holding out 30% instead of 40% raises the .30/.90 target to 588 expected recruits;
30% attrition at 40% holdout raises it to 505. Attrition inflation assumes noninformative
loss and is an expectation, not a guarantee that 141 complete holdout people will remain.

Freeze an actual source-specific recruitment cap/stopping rule and N before outcome
access. Report achieved N and exclusions without endpoint-dependent top-ups. If the
cap produces fewer complete pairs, report reduced precision and model-based detectable
effects; do not claim validation. Published small archival cohorts may be useful for
exploratory feasibility and cannot satisfy the planned confirmatory N merely by
repeating trials. Missing outcome values are not imputed as failures/successes; the
primary estimand is complete paired observations, with missingness and potential
selection bias reported. Missingness patterns and worst-case descriptive bounds are
secondary; evidence of informative missingness limits generalization.

The synthetic `48/1296=3.7037%` is the fraction of a uniformly enumerated mathematical
grid, **not clinical prevalence**. It enters none of these calculations. Testing a
perfectly error-free prevalence null `p=0` by observing one event is a different,
degenerate detection question and does not establish a clinical effect. Any future
prevalence design needs a nonzero background/error rate, an independent measurement
definition, precision targets, and its own prespecified model.

## Source, ethics, consent, and safety gates

All gates remain closed for real-data execution in R2B:

1. **Source and rights:** named independent custodian, provenance, data dictionary,
   permitted secondary use, lawful transfer/storage basis, documented consent scope
   or an independently approved waiver, permitted retention and publication rights.
2. **Within-person coverage:** verify every required task, chronology, delay, direct
   versus proxy measurement, reliability, norms, sample independence and duplicate
   records in an approved private environment. Public article descriptions do not
   certify file contents. Insufficient source coverage means HOLD, with no invented
   variables, inferred consciousness labels, or pooled task summaries treated as rows.
3. **Ethics and capacity:** independent ethics committee approval before new recruitment
   or secondary use as applicable; accessible consent and capacity evaluation by
   qualified staff; legally valid representative consent where required plus participant
   assent and respect for dissent/withdrawal. No enrolling a person merely because
   they cannot object. Research participation has no effect on ordinary care.
4. **Prospective lock:** publicly register protocol and source-specific supplement
   before new recruitment and before any access to individual outcomes for an archival
   study; preserve dated amendments and disclosure of previously known summaries.
5. **Privacy and safety:** approved private storage, minimum necessary fields, roles,
   audit trail and deletion/retention policy; never publish rows, health identifiers,
   raw narratives, or email contents. Stop/offer breaks for distress, fatigue or
   withdrawal. Qualified investigators manage unexpected clinical concerns through
   existing care procedures; this research script supplies no diagnosis or advice.
6. **Execution:** present R2B CLI accepts no participant file. A future approved private
   analysis implementation requires separate review and cannot be activated by changing
   a JSON Boolean. No live screening, production model/weights, interventions, health
   records, or automatic data transfer is authorized by this plan.

Issue [#13](https://github.com/Hawkar-usls/Simptomat/issues/13) records the first Teghil
request as sent, awaiting external response. R2B sends no second letter and performs no
patient-data extraction. No new response or data receipt has been verified here.

## Prior literature and interpretation boundaries

The `p=.15`, n=11/13 result discussed in R2 is a published summary, not a reanalysis.
Nonsignificance with small samples and no prespecified equivalence margin is inconclusive;
it proves neither equivalence nor absence of an effect. It also does not, by itself,
establish that a study had insufficient power: power depends on the effect and model.
Teghil et al.'s availability-on-request statement is not permission, receipt, coverage,
or qualification of participant-level data. Scientific status remains
**HOLD_NO_INDEPENDENT_PARTICIPANT_LEVEL_VALIDATION** after engineering success.

Method references: [NCSS paired t-test assumptions/effect size](https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/PASS/Paired_T-Tests_using_Effect_Size.pdf),
[Minitab noncentral-t power formulas](https://support.minitab.com/en-us/minitab/help-and-how-to/statistics/power-and-sample-size/how-to/hypothesis-tests/power-and-sample-size-for-paired-t/methods-and-formulas/methods-and-formulas/),
[WMA Declaration of Helsinki](https://www.wma.net/policies-post/wma-declaration-of-helsinki/),
[WHO prospective registration](https://www.who.int/tools/clinical-trials-registry-platform/network/trial-registration).
These support methods/ethics principles; they do not validate this proposed instrument,
its effect assumptions, or the JANUS hypothesis.
