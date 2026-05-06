# Task: s45

**Title.** Impact of Class Size Cap Policy on Reading Scores

## Research question

This study investigates the effect of implementing a class size cap policy on students' reading scores in elementary schools. Specifically, it examines whether reducing class sizes leads to changes in reading performance, measured in standard deviation units.

## Data description

The dataset includes 100 observations from various schools, with columns for unit_id representing each school, period indicating the academic year, treated as a binary indicator of whether the school was subject to the class size cap policy, post indicating the period after policy implementation, treat_x_post as the interaction term, and y representing the reading scores in SD units.

**Data file path.** `experiments/exp_b/data/s45_data.csv`

## Data preview (first rows)

```
 unit_id  period  treated  post  treat_x_post       y
       0       1        1     0             0  1.9476
       1       1        1     0             0  0.6716
       2       1        1     0             0  1.0359
       3       1        1     0             0  0.5329
       4       1        1     0             0 -0.3832
```

## Column types

```
  unit_id: int64
  period: int64
  treated: int64
  post: int64
  treat_x_post: int64
  y: float64
```

## Output requirement

Your R script must print exactly one line in this format:

```r
cat("treatment_effect_estimate:", estimate, "\n")
```

Save the script at `audit/human_coder_baseline/submissions/s45_submission.R`.
