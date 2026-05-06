# Task: s51

**Title.** Impact of Earnings Announcements on Stock Returns

## Research question

Do quarterly earnings announcements lead to abnormal stock returns? Specifically, we aim to measure the immediate impact of these announcements on the stock prices of publicly traded companies. Understanding this effect is crucial for investors seeking to optimize their portfolio strategies around these events.

## Data description

The dataset comprises 100 publicly traded companies, each with daily stock return data around the time of their quarterly earnings announcements. Key columns include stock_id, event_day, ret (daily stock return), mkt_ret (market return), and beta (stock's sensitivity to market movements).

**Data file path.** `experiments/exp_b/data/s51_data.csv`

## Data preview (first rows)

```
 stock_id  event_day       ret   mkt_ret   beta
        0        -10  0.000405  0.006407 1.2108
        0         -9 -0.006114 -0.002840 1.2108
        0         -8 -0.007431 -0.005155 1.2108
        0         -7 -0.011608 -0.002246 1.2108
        0         -6  0.000127 -0.001106 1.2108
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

Save the script at `audit/human_coder_baseline/submissions/s51_submission.R`.
