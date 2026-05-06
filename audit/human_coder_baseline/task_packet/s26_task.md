# Task: s26

**Title.** Test score cutoff and college enrollment

## Research question

Does crossing a test score threshold for automatic college admission increase actual enrollment rates?

## Data description

Cross-sectional data on 600 high school graduates. Variables: running_var (standardized test score, 0–1; cutoff = 0.5), treated (1 if score ≥ cutoff), y (enrolled in college binary as continuous proxy), near_cutoff (within ±0.3 bandwidth). Sharp RDD.

**Data file path.** `experiments/exp_b/data/s26_data.csv`

## Data preview (first rows)

```
 running_var  treated       y  near_cutoff
      0.4277        0  0.2428            1
      0.2368        0 -0.0894            1
      0.7100        1  0.3405            1
      0.3737        0 -0.1025            1
      0.8747        1  0.4601            0
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

Save the script at `audit/human_coder_baseline/submissions/s26_submission.R`.
