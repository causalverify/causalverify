# Task: s21

**Title.** Vietnam draft lottery as IV for military service on earnings

## Research question

Did military service reduce long-run civilian earnings, using Vietnam-era draft lottery numbers as an instrument for veteran status?

## Data description

Cross-sectional data on 500 men eligible for Vietnam-era draft. Variables: y (log annual earnings), x (veteran binary), z (draft lottery number, 1–365; low numbers = likely drafted), controls (age, education, race). IV: low draft number → more likely to serve → instrument for veteran status.

**Data file path.** `experiments/exp_b/data/s21_data.csv`

## Data preview (first rows)

```
      y       x  z  controls
-0.1677 -0.1319  0    1.2676
 1.0292  0.7080  0   -0.8820
 0.1937  1.1326  1   -0.5251
-0.4724  0.2380  1   -0.8178
 0.4748  0.3501  0   -1.7332
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

Save the script at `audit/human_coder_baseline/submissions/s21_submission.R`.
