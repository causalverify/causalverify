# Task: s98

**Title.** Impact of Covenant Violations on Capital Expenditure

## Research question

How does crossing a debt-to-asset covenant threshold affect a firm's capital expenditure decisions? Specifically, we are interested in understanding whether firms increase their capital expenditures when they are just above or below this financial covenant threshold.

## Data description

The dataset includes 400 firms, with columns for running_var (representing the debt-to-asset ratio), treated (indicating whether the firm is above the covenant threshold), and y (log capex, the outcome of interest). The data focuses on firms near the covenant violation threshold, allowing for a detailed analysis of their investment behavior.

**Data file path.** `experiments/exp_b/data/s98_data.csv`

## Data preview (first rows)

```
 running_var  treated       y  near_cutoff
      0.8395        1  0.3456            0
      0.3581        0 -0.0625            1
      0.1659        0 -0.0031            0
      0.3722        0 -0.0589            1
      0.9009        1  0.3356            0
```

## Column types

```
  running_var: float64
  treated: int64
  y: float64
  near_cutoff: int64
```

## Output requirement

Your R script must print exactly one line in this format:

```r
cat("treatment_effect_estimate:", estimate, "\n")
```

Save the script at `audit/human_coder_baseline/submissions/s98_submission.R`.
