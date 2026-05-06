# Task: s77

**Title.** Impact of Road Density on Urban Population Growth

## Research question

How does road density influence population growth in urban areas? Specifically, can the 1947 highway plan be used as an instrumental variable to assess the causal effect of increased road density on population growth?

## Data description

The dataset includes 400 urban areas with columns for population growth (y), road density (x), the 1947 highway plan as an instrumental variable (z), and other control variables (controls) such as median income and education level. The data spans several decades, capturing variations in road development and demographic changes.

**Data file path.** `experiments/exp_b/data/s77_data.csv`

## Data preview (first rows)

```
      y       x  z  controls
 0.7249  0.5475  1   -0.0822
-0.0817 -0.2227  0   -0.2445
-1.1538 -0.4352  0    0.3557
 0.7176  0.7494  0   -0.4956
-0.1182 -0.1524  0   -0.9614
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

Save the script at `audit/human_coder_baseline/submissions/s77_submission.R`.
