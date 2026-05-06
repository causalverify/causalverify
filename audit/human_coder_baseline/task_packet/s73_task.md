# Task: s73

**Title.** Impact of Immigration on Native Wages

## Research question

How does an increase in immigrant inflow affect the wages of native workers? The study leverages historical settlement patterns as an instrumental variable to address potential endogeneity in immigrant distribution.

## Data description

The dataset consists of 400 observations, with columns including 'y' for native wages, 'x' for immigrant inflow, 'z' for historical settlement patterns, and 'controls' for demographic and economic factors. The data captures variations in immigrant inflow influenced by historical settlement patterns.

**Data file path.** `experiments/exp_b/data/s73_data.csv`

## Data preview (first rows)

```
      y       x  z  controls
 0.6794  0.1961  0   -1.9624
 1.4609  0.9742  0   -0.2953
-1.5803 -1.0906  0   -1.0845
 0.4529  0.8094  0   -1.0326
 0.1509  0.6119  1   -1.3879
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

Save the script at `audit/human_coder_baseline/submissions/s73_submission.R`.
