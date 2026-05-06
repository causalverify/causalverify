# Task: s60

**Title.** Impact of Unexpected Dovish Fed Announcements on Bank Stock Returns

## Research question

How do unexpected dovish announcements by the Federal Reserve affect cumulative abnormal returns (CAR) of bank stocks? This study aims to understand the immediate market reaction to such monetary policy surprises.

## Data description

The dataset includes daily stock return data for 80 banks, with columns: stock_id, event_day, ret, mkt_ret, and beta. Event_day captures the days surrounding the Fed announcement, allowing for the analysis of stock returns before and after the event.

**Data file path.** `experiments/exp_b/data/s60_data.csv`

## Data preview (first rows)

```
 stock_id  event_day       ret   mkt_ret   beta
        0        -10  0.048920  0.020246 1.3315
        0         -9 -0.016727 -0.003478 1.3315
        0         -8  0.011121 -0.015632 1.3315
        0         -7  0.032321  0.010543 1.3315
        0         -6 -0.016388 -0.005134 1.3315
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

Save the script at `audit/human_coder_baseline/submissions/s60_submission.R`.
