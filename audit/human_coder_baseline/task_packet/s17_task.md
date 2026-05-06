# Task: s17

**Title.** Surprise regulatory fine on bank reputation and stock value

## Research question

Does a surprise regulatory fine announcement generate negative abnormal returns beyond the direct financial cost (fine amount / market cap), suggesting reputational damage?

## Data description

Event study data for 80 banks. Variables: stock_id, event_day (−10 to +10), ret, mkt_ret, beta, fine_ratio (fine/mktcap). Evaluate if CAR < −fine_ratio, implying reputational loss beyond the fine itself. Market model: [−10,−2]. Event window [−1,+1].

**Data file path.** `experiments/exp_b/data/s17_data.csv`

## Data preview (first rows)

```
 stock_id  event_day       ret   mkt_ret   beta
        0        -10 -0.012327  0.010128 1.2914
        0         -9  0.016638 -0.002574 1.2914
        0         -8 -0.023026 -0.014942 1.2914
        0         -7 -0.008155 -0.001852 1.2914
        0         -6  0.036959  0.014059 1.2914
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

Save the script at `audit/human_coder_baseline/submissions/s17_submission.R`.
