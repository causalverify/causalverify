# Task: s18

**Title.** Contaminated event window: confounding news during event period

## Research question

A firm announced both an acquisition AND an earnings beat on the same day. Can we decompose the market reaction to isolate the acquisition effect from the confounding earnings news?

## Data description

Event study data for 80 firms with simultaneous announcements. Variables: stock_id, event_day (−10 to +10), ret, mkt_ret, beta, eps_surprise. Challenge: earnings surprise on day 0 confounds acquisition announcement. Approach: partial out eps_surprise in the AR regression.

**Data file path.** `experiments/exp_b/data/s18_data.csv`

## Data preview (first rows)

```
 stock_id  event_day       ret   mkt_ret   beta
        0        -10  0.032755 -0.002721 1.1919
        0         -9  0.009170  0.011178 1.1919
        0         -8  0.009466 -0.002584 1.1919
        0         -7 -0.023236 -0.004374 1.1919
        0         -6 -0.031605  0.001126 1.1919
```

## Column types

```
  stock_id: int64
  event_day: int64
  ret: float64
  mkt_ret: float64
  beta: float64
```

## Output requirement

Your R script must print exactly one line in this format:

```r
cat("treatment_effect_estimate:", estimate, "\n")
```

Save the script at `audit/human_coder_baseline/submissions/s18_submission.R`.
