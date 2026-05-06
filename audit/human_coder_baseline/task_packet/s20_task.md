# Task: s20

**Title.** Distance to bank as IV for savings rate

## Research question

Does having a bank account increase household savings, using distance to the nearest bank branch as an instrument for account ownership?

## Data description

Cross-sectional data on 500 households. Variables: y (monthly savings in USD), x (has_account binary), z (distance to nearest branch in km — instrument), controls (income, education). First stage: distance → account ownership (negative). Exclusion: distance affects savings only through account ownership.

**Data file path.** `experiments/exp_b/data/s20_data.csv`

## Data preview (first rows)

```
      y       x  z  controls
-0.2712  0.2625  1    0.4520
 0.3464  0.8995  1   -1.0999
 0.6999  0.5116  0    0.8467
-0.4331 -0.0623  0    0.1562
-2.3853 -1.4952  1   -0.1289
```

## Column types

```
  y: float64
  x: float64
  z: int64
  controls: float64
```

## Output requirement

Your R script must print exactly one line in this format:

```r
cat("treatment_effect_estimate:", estimate, "\n")
```

Save the script at `audit/human_coder_baseline/submissions/s20_submission.R`.
