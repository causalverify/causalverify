# Human Baseline for CausalVerify L2b+

**Purpose.** Establish a human-expert baseline against which LLM L2b+
pass rates are interpretable. Without a human number, "Opus reaches
~88% L2b+ pass" is uninterpretable: 88% could be near-ceiling or
mediocre depending on what a trained econometrics graduate student
would achieve on the same task.

**Why this matters.** Reviewer concern (NeurIPS D&B): the absolute
L2b+ rates we report (10%–88% across six models) sit in an
interpretive vacuum. A 10-paper human baseline (5–10 students × 8
scenarios) lets us anchor model performance on a familiar reference
point. Even an N=5 student baseline gives the paper a defensible
"models match / lag / exceed entry-level human" framing.

This directory contains everything needed to recruit, instruct,
score, and report the human baseline. **No LLM cost; only human
time.**

## Files

```
experiments/exp_a_human_baseline/
├── README.md                      # this file (overview)
├── instructor_packet.md           # what the researcher running the
│                                  # study does (recruit, instruct,
│                                  # collect, score)
├── student_packet_template.md     # what each student gets — paste
│                                  # the relevant scenario block in
├── scoring_rubric.md              # how to score student submissions
│                                  # using the same L2b+ pipeline
│                                  # used for LLMs
├── scenario_set.json              # the 8 chosen scenarios + the
│                                  # canonical β̂ baseline each
│                                  # student's R code is compared to
└── score_humans.py                # turnkey scorer: takes student
                                   # R scripts, runs them through
                                   # L1 / L2a / L2b / L2b+ identically
                                   # to LLM scoring, writes
                                   # human_baseline_scores.csv
```

## Headline protocol

1. **Recruit** 5–10 econometrics graduate students with R experience.
2. **Brief**: each student gets the `student_packet_template.md`
   instantiated for the 8 stratified scenarios (2 per method family,
   4 easy + 4 medium). Total time per student: ~2–4 hours.
3. **Submit**: students return one R script per scenario, named
   `<scenario_id>_<student_id>.R`. No discussion among students.
4. **Score**: run `python3 score_humans.py --submissions <dir>`. The
   script invokes the same `score_l2b_plus.py --baseline canonical`
   path used for LLMs, with the same Haiku-based judge extraction.
5. **Report**: per-student, per-method aggregate L2b+ pass rate.
   Cross-tabulate against LLM pass rates in the paper appendix.

## What this baseline tests

Same task as LLMs:
- Read the research question + data description + 5-row CSV preview.
- Write an R script that estimates the treatment effect.
- The R script must run, produce an estimated coefficient, and the
  estimate must match the canonical estimator on the realised
  dataset within ±50% relative error (same threshold as L2b+).

## What this baseline does NOT test

- Real research diagnostics (parallel-trends checks, robustness
  sweeps, weak-instrument F-tests). Like the LLM evaluation, this is
  a one-shot specification task.
- Method *choice* under uncertainty. Like the LLM evaluation, the
  scenario already implies a method via the data structure; the test
  is whether the student writes the textbook regression for it.

## Time budget for the researcher

| Step | Time |
|---|---|
| Recruit (5–10 students) | 1–2 days, async |
| Brief + distribute packets | 30 min |
| Wait for submissions | 1–2 weeks |
| Run scorer + tabulate | 30 min |
| **Total researcher time** | **~3 hours active** |

## Reporting in the paper

Add to `paper/latex/neurips_v11.tex`:

> **Human baseline.** We collected R-code submissions from N graduate
> students (econometrics PhD year 2–4, all with prior R experience)
> on 8 stratified Exp B scenarios. Per-scenario submissions were
> scored using the same L2b+ pipeline (canonical-baseline judge
> extraction). The aggregate human L2b+ pass rate is X% (95% CI
> [Y, Z]); the same students average M% on easy scenarios and N% on
> medium scenarios. Six frontier LLMs achieve a range of A%–B% on the
> same set. \textbf{Reading}: Opus's 88% L2b+ rate is approximately
> [comparable to / above / below] the human-graduate-student baseline
> on this task.
