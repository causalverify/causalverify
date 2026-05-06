# Task: s52

**Title.** Impact of M&A Announcements on Stock Returns

## Research question

How do merger and acquisition announcements affect the cumulative abnormal returns of the involved companies? We aim to quantify the immediate impact of these announcements on stock performance.

## Data description

The dataset comprises daily stock returns for 100 companies around the time of merger announcements. Key columns include stock_id, event_day, ret, mkt_ret, and beta, capturing stock returns, market returns, and the event window day relative to the announcement.

**Data file path.** `experiments/exp_b/data/s52_data.csv`

## Data preview (first rows)

```
 stock_id  event_day       ret   mkt_ret   beta
        0        -10 -0.024554 -0.007205 0.8878
        0         -9 -0.010282  0.000896 0.8878
        0         -8  0.004361  0.006214 0.8878
        0         -7 -0.013523 -0.002826 0.8878
        0         -6  0.021205  0.014607 0.8878
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

Save the script at `audit/human_coder_baseline/submissions/s52_submission.R`.
