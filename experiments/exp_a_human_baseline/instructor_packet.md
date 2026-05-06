# Instructor Packet — Human Baseline Study

For the **researcher / instructor / advisor** running the human-baseline
data collection. Self-contained: students never see this file.

## Step 0 — Sanity check (5 min)

The 8 chosen scenarios + the canonical β̂ each one is compared
against are in `scenario_set.json`. Open it once and skim the titles
to make sure no scenario is on a politically sensitive topic that
would require IRB review at your institution. (Current set is
benign: COVID lockdowns, TARP, Fed rate hikes, M&A, rainfall as IV,
draft lottery, vote-share cutoff, income subsidies. None require
IRB.)

## Step 1 — Recruit students (1–2 days, async)

Target: **5–10 econometrics PhD students, year 2–4**, with prior R
experience. Pool: your own students, your colleague's students,
econometrics workshops at your institution.

Suggested recruitment text (paste in Slack / email):

> Subject: Quick R-coding task (~15–30 min × 8 = 2–4 hours, paid /
> co-author / acknowledgment depending on availability)
>
> Hi all, I'm running a small benchmark study comparing how
> economics graduate students do on standardized causal-inference
> coding tasks vs. how frontier LLMs (Opus, GPT, etc.) do. I need
> ~8 R scripts per participant from 5–10 of you. Each script
> implements the textbook regression for a given research scenario.
> Compensation: [$50 / acknowledgment / ...].
>
> No discussion among participants until after submission. Reply if
> interested.

**Important**: tell students they should **not** discuss the
scenarios with each other before submitting. The point is to measure
*independent* baseline performance, not collective wisdom.

## Step 2 — Distribute (15 min)

For each student:
1. Pick a unique student ID (e.g., `S01`, `S02`, ..., or randomized
   3-letter codes if you want anonymity).
2. Open `student_packet_template.md` in this folder.
3. Replace the `<<STUDENT_ID>>` placeholder with the student's ID.
4. Send them the filled-in template + a deadline (suggest: 1 week
   minimum, 2 weeks generous).

Optional (recommended for fairness with LLM): tell students they may
use any reference material (Wooldridge, Angrist-Pischke, Stack
Overflow), but **may not use an LLM** for code generation.
Scientifically the comparison is: human-with-textbook vs.
LLM-without-other-tools. (If you want to also include
human-with-LLM, that's a 3rd arm; out of scope for this baseline.)

## Step 3 — Collect (1–2 weeks, async)

Each student returns 8 R scripts named:

```
s01_<STUDENT_ID>.R   # COVID lockdown × foot traffic
s04_<STUDENT_ID>.R   # TARP × bank risk
s11_<STUDENT_ID>.R   # Fed rate hike × bank stocks
s13_<STUDENT_ID>.R   # M&A announcement returns
s19_<STUDENT_ID>.R   # Rainfall as IV
s21_<STUDENT_ID>.R   # Draft lottery as IV
s25_<STUDENT_ID>.R   # Vote share cutoff
s27_<STUDENT_ID>.R   # Income cutoff for subsidy
```

Save them under
`experiments/exp_a_human_baseline/submissions/<STUDENT_ID>/`.

## Step 4 — Score (30 min)

```bash
python3 experiments/exp_a_human_baseline/score_humans.py \
    --submissions experiments/exp_a_human_baseline/submissions/ \
    --out         experiments/exp_a_human_baseline/human_baseline_scores.csv
```

The scorer:
- Runs each `*.R` file with `Rscript --vanilla` (same as LLM L2b)
- Sends the stdout to the same Haiku-based judge that scores LLMs
- Compares the extracted β̂ to the canonical baseline in
  `scenario_set.json` (same ±50% tolerance)
- Outputs per-student, per-scenario L1 / L2a / L2b / L2b+ pass /
  fail, identical schema to `l2b_plus_scores_canonical_judge_v2.csv`

## Step 5 — Tabulate and report (30 min)

The scorer also writes a small summary:

| Student | DID | Event Study | IV | RDD | Overall |
|---------|-----|-------------|----|----|---------|
| S01     | 2/2 | 1/2         | 2/2| 2/2| 7/8     |
| ...     |     |             |    |    |         |

For the paper, report:
- Per-student L2b+ rate (mean and 95% CI across scenarios)
- Per-method human L2b+ rate (mean across students)
- Compare to per-model LLM L2b+ rates from `l2b_plus_summary_canonical_judge_v2.json`

## Notes for the instructor

- **Do not give students the canonical β̂.** They get the same
  prompt LLMs got: research question + data description + 5-row CSV
  preview. The canonical β̂ is the answer key, which only the scorer
  sees.
- **Do not let students work in groups.** The L2b+ pass rate must
  reflect individual-attempt performance.
- **One R script per scenario per student.** No multiple submissions.
  If a student wants to revise, they overwrite their previous file.
- **It is OK if some students fail.** The point is to measure
  baseline performance, not optimize for it.
