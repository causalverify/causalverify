# R-Coding Task — Causal Inference Benchmark

**Student ID:** `<<STUDENT_ID>>`
**Deadline:** `<<DEADLINE>>`
**Estimated time:** 2–4 hours total (15–30 min per scenario × 8)

## What you are doing

For each of 8 research scenarios below, you are given:
1. A **research question** (a few sentences),
2. A **data description** (column names, sample size, unit of
   observation, treatment definition),
3. A **5-row preview** of the data CSV (first 5 rows),
4. The **path to the full CSV file** on disk.

You must write **one R script per scenario** that:
- Loads the CSV from the given path,
- Implements the **standard textbook causal-inference regression**
  appropriate for the scenario (DID, event study, IV, or RDD; you
  decide based on the data structure),
- Prints the **estimated treatment-effect coefficient** to standard
  output in a clearly recognizable format (a labeled `cat()` line is
  fine, e.g., `cat("treatment_effect:", coef, "\n")`).

## Rules

- Use any textbook reference (Wooldridge, Angrist-Pischke,
  Mostly-Harmless, Stack Overflow). **Do not use an LLM** (ChatGPT,
  Claude, Copilot, etc.) for code generation.
- No collaboration with other participants until after submission.
- One submission per scenario per student. If you revise, overwrite
  the previous file.
- Save scripts as `s<NN>_<<STUDENT_ID>>.R` (e.g.,
  `s01_S03.R` for student S03 working on scenario s01) and email
  them all back together when done.

## What gets scored

Your script is run with `Rscript --vanilla` against the same CSV the
LLMs saw. We check:
- L1: Did your script produce any output?
- L2a: Does your script contain R code? (Trivially yes since it's a
  `.R` file.)
- L2b: Does your script run without an error?
- L2b+: Does your script's printed treatment-effect coefficient match
  the canonical estimator on the realised dataset within ±50%?

You will not be told the canonical answer until after the study
closes.

## Recommended R packages

`fixest`, `AER`, `rdrobust`, `ivreg`, `lmtest`, `sandwich`. All are
on CRAN. Make sure your code runs in a clean R session
(`Rscript --vanilla` does not load `.Rprofile`).

---

## Scenario 1 — `s01` (DID, easy)

**Title.** COVID-19 lockdown effect on retail foot traffic

**Research question.**
> Did COVID-19 lockdown orders (March 2020) reduce retail store foot
> traffic, and did stores in counties with stricter lockdowns
> experience larger declines compared to stores in counties with
> minimal restrictions?

**Data description.**
> Panel data on 200 retail stores across 8 monthly periods
> (2019M10–2020M5). Variables: `unit_id` (store), `period` (1–8,
> treatment at period 4 = March 2020), `treated` (1 = county with
> strict lockdown, 0 = minimal restrictions), `post` (1 = post-March
> 2020), `treat_x_post` (interaction), `y` (log foot traffic index).
> Pre-period: 3 months. Post-period: 5 months.

**CSV path.** `experiments/exp_b/data/s01_data.csv`

**5-row preview.**
```
unit_id,period,treated,post,treat_x_post,y
0,1,1,0,0,0.0714
1,1,1,0,0,1.1954
2,1,1,0,0,-0.7364
3,1,1,0,0,0.3802
4,1,1,0,0,0.4023
```

---

## Scenario 2 — `s04` (DID, medium)

**Title.** TARP capital injection on bank risk-taking

**Research question.**
> Did TARP capital injections (2008–2009) cause recipient banks to
> increase risk-taking (measured by non-performing loan ratio)
> compared to non-recipient banks?

**Data description.**
> Panel data on 200 bank holding companies over 8 quarterly periods
> (2007Q3–2009Q2). Variables: `unit_id` (bank), `period`, `treated`
> (1 = TARP recipient), `post` (1 = post-TARP), `treat_x_post`,
> `y` (non-performing loan ratio). TARP recipients self-selected
> — use parallel pre-trends as identifying assumption.

**CSV path.** `experiments/exp_b/data/s04_data.csv`

(See file for the 5-row preview when you open it.)

---

## Scenario 3 — `s11` (Event Study, easy)

**Title.** Fed rate hike announcement on bank stock returns

**Research question.**
> Does an unexpected Fed rate-hike announcement cause negative
> abnormal returns on bank stocks in the days surrounding the
> announcement?

**Data description.**
> 80 publicly listed U.S. bank stocks observed for 21 days
> surrounding an FOMC announcement day (event_day ∈ [-10, +10]).
> Variables: `stock_id`, `event_day`, `ret` (daily return),
> `mkt_ret` (market return), `beta` (each stock's market beta). The
> announcement (event_day = 0) is the rate-hike news.

**CSV path.** `experiments/exp_b/data/s11_data.csv`

---

## Scenario 4 — `s13` (Event Study, medium)

**Title.** M&A announcement returns for acquirer firms

**Research question.**
> Do M&A announcements generate negative abnormal returns for
> acquiring firms in the announcement window, on average?

**Data description.**
> 80 acquiring firms × 21 event-day observations. Same column
> structure as a market-model event study; treatment is `event_day
> >= 0`.

**CSV path.** `experiments/exp_b/data/s13_data.csv`

---

## Scenario 5 — `s19` (IV, easy)

**Title.** Rainfall as IV for agricultural loan demand

**Research question.**
> Does agricultural-sector lending volume causally respond to
> regional agricultural income, using rainfall as an instrument
> for income?

**Data description.**
> 500 region-year observations. Variables: `y` (loan demand),
> `x` (agricultural income, endogenous), `z` (rainfall index,
> instrument), `controls` (a control covariate).

**CSV path.** `experiments/exp_b/data/s19_data.csv`

---

## Scenario 6 — `s21` (IV, medium)

**Title.** Vietnam draft lottery as IV for military service on
earnings

**Research question.**
> Did serving in the Vietnam War reduce subsequent civilian
> earnings, using the draft lottery number as an instrument for
> military service?

**Data description.**
> 500 individual-level observations. Variables: `y` (log earnings
> in 1981 dollars), `x` (Vietnam-era military service indicator,
> endogenous), `z` (draft-lottery instrument, eligibility based on
> birthday), `controls`.

**CSV path.** `experiments/exp_b/data/s21_data.csv`

---

## Scenario 7 — `s25` (RDD, easy)

**Title.** Vote share cutoff and policy adoption

**Research question.**
> Does narrow-margin election of a Democratic candidate (>50% vote
> share) cause policy adoption?

**Data description.**
> 600 election observations. Variables: `running_var` (vote share),
> `treated` (1 if running_var ≥ 0.5), `y` (binary policy adoption
> outcome), `near_cutoff` (within bandwidth of 0.3).

**CSV path.** `experiments/exp_b/data/s25_data.csv`

---

## Scenario 8 — `s27` (RDD, medium)

**Title.** Income cutoff and subsidy program participation

**Research question.**
> Does income falling below the program-eligibility cutoff cause
> participation, with effects estimated by sharp regression
> discontinuity?

**Data description.**
> Cross-section, ~600 households. Variables: `running_var`
> (household income normalized so cutoff = 0.5), `treated`
> (1 if eligible), `y` (program take-up rate or subsidized
> outcome), `near_cutoff`.

**CSV path.** `experiments/exp_b/data/s27_data.csv`

---

## Submission

When all 8 scripts are written, send them as a zip / folder to:
`<<INSTRUCTOR_EMAIL>>`

with subject line: `CausalVerify human baseline — <<STUDENT_ID>>`.

Thank you! Your time helps anchor a benchmark of frontier LLMs
against a real human reference point.
