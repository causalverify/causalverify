# Task: s88

**Title.** Impact of Close-Election Incumbency on Reelection Probability

## Research question

Does winning a close election affect the probability of an incumbent being reelected in subsequent elections? Specifically, we investigate whether incumbents who barely win an election are more or less likely to win reelection compared to those who barely lose.

## Data description

The dataset contains information on 600 elections, with columns for running_var (vote-share margin), treated (whether the incumbent won the close election), and y (reelection probability). The data focuses on elections where the vote-share margin was within a narrow range around the cutoff for winning.

**Data file path.** `experiments/exp_b/data/s88_data.csv`

## Data preview (first rows)

```
 running_var  treated       y  near_cutoff
      0.8265        1  0.4212            0
      0.6432        1  0.2540            1
      0.9944        1  0.4064            0
      0.9578        1  0.6436            0
      0.0211        0 -0.1036            0
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

Save the script at `audit/human_coder_baseline/submissions/s88_submission.R`.
