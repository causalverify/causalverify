# Scoring Rubric — Human Baseline

This is the explicit grading scheme `score_humans.py` implements. The
intent is **byte-for-byte equivalence with the LLM L2b+ pipeline**
so the human-vs-LLM comparison is apples-to-apples.

## Layers

| Layer | Question | Pass condition |
|-------|----------|----------------|
| L1    | Did the script produce any output? | Non-empty stdout |
| L2a   | Does the script contain R code? | File ends in `.R` and is non-empty (trivially yes here) |
| L2b   | Does the script run without error under `Rscript --vanilla`? | Exit code 0 and no fatal error |
| L2b+  | Does the printed coefficient match the canonical β̂ within ±50%? | `|β̂_student − β̂_canonical| / |β̂_canonical| < 0.5` |
| L4    | Does the student's printed direction agree with the canonical direction? | Sign(β̂_student) matches sign(β̂_canonical) |

L3 (method-family agreement) is not scored here because each scenario
already specifies the method family in its description; the student is
not asked to choose a method family. We do not penalise the student
for using a slightly different but equivalent specification (e.g.,
`feols` vs. `lm` with manual fixed-effect dummies for DID); only the
final coefficient matters.

## Coefficient extraction

Identical to the LLM pipeline:
1. Capture full stdout from `Rscript --vanilla`.
2. Pass stdout + the executed R code + the scenario's method family
   as context to a Haiku-based judge that returns:
   ```
   {"effect": <number or null>, "rationale": "..."}
   ```
3. The judge's output is the student's β̂. If the judge returns null,
   the script is treated as having no extractable coefficient and L2b+
   fails (matching the LLM treatment of unparseable outputs).

We use the LLM judge rather than a regex precisely because student
print formats vary (some `cat()`, some `print(coef(model))`, some
just print the model summary). The judge is robust to this variation
in the same way it is for LLMs.

## ES window-aware matching

For Event Study scenarios (s11, s13), we accept any of the standard
post-event window aggregations as a valid match: per-day average AR,
2-day CAR[0,+1], 3-day CAR[0,+2], 5-day CAR[0,+4], 10-day CAR[0,+9],
or 11-day CAR[0,+10]. The match passes if the student's coefficient is
within tolerance of any of these. This mirrors the
`recompute_l2b_plus_es_aware.py` logic used for LLM scoring.

## Per-student aggregation

For each student we report:
- L2b+ pass rate overall (number of scenarios passed / 8)
- L2b+ pass rate by method family (DID 0/2..2/2, ES 0/2..2/2, IV 0/2..2/2, RDD 0/2..2/2)
- L2b+ pass rate by difficulty (easy 0/4..4/4, medium 0/4..4/4)
- Mean and 95% CI across students (Wilson interval)

## Reporting in the paper

Three numbers go in the paper:
- **Headline.** Aggregate human L2b+ pass rate (across all
  student × scenario cells), with 95% CI.
- **Per-method.** Human L2b+ rate per method family.
- **Comparison.** Side-by-side table: per-method LLM rates (from
  `l2b_plus_summary_canonical_judge_v2.json`) vs. human rates.

Three things to be careful about:

1. The human number is from a **different protocol** (independent
   submissions, no LLM assistance). The number is comparable in the
   sense that the *task* and the *scoring* are identical, but the
   *cognitive process* differs, and the human pool is not a
   representative sample of "all econometrics PhDs."

2. Human L2b+ rate at, say, 75% does not mean LLM-at-88% is
   "superhuman." A reasonable read is "Opus operates within the
   range of a competent econometrics graduate student on this
   restricted task."

3. The human number is N=5–10, on 8 scenarios, so ~40–80 attempts;
   bootstrapped CIs on a per-method rate will be wide. Report wide
   CIs honestly.
