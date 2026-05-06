# Human Coder Baseline (Exp B)

This directory holds the scaffold for a human-coder baseline on a
stratified subset of Exp B scenarios. **It is distinct from
`audit/l2b_judge_human_validation/`**, which validates the
*coefficient-extraction judge*, not the upstream coder.

## Purpose

The baseline is a **solvability audit**, not a population estimate of
expert performance. It asks: when given the same scenario brief that an
LLM received, can a trained human coder write R that executes (L2b) and
recovers the canonical estimator on the realised dataset within the
paper's tolerance (L2b+)?

## Blinding

The human coder sees only what the LLMs saw: scenario title, research
question, data description, CSV path, data preview, column types. The
coder does NOT see:

- the canonical estimator's output (`audit/dgp_verification.json`),
- the L2b+ pass label (`experiments/exp_b/l2b_plus_*.csv`),
- the DGP truth parameter (`dgp_truth.effect` / `direction`),
- any LLM model output, judge output, or per-cell score.

Manifest at `task_packet/manifest.json` records the blinding state
explicitly.

## Layout

```
audit/human_coder_baseline/
├── README.md                  # this file
├── task_packet/
│   ├── INSTRUCTIONS.md        # general task brief
│   ├── manifest.json          # sampled scenario IDs + blinding flags
│   └── s<NN>_task.md          # one task brief per scenario (blinded)
├── submissions/
│   └── s<NN>_submission.R     # placeholders until human coder commits
├── summary.json               # written by the scorer; status field set
└── summary.md                 # human-readable mirror of summary.json
```

## How to use

1. Generate the packet (deterministic, no API calls):

   ```bash
   python3 scripts/prepare_human_coder_baseline.py --n 20 --seed 20260505
   ```

2. The human coder reads each `task_packet/s<NN>_task.md` and replaces
   the placeholder in `submissions/s<NN>_submission.R` with a standalone
   R script. Each script must print exactly one line in the format:

   ```r
   cat("treatment_effect_estimate:", estimate, "\n")
   ```

3. Score the submitted scripts (executes R, no API calls, no frozen
   artifact modified):

   ```bash
   python3 scripts/score_human_coder_baseline.py
   ```

   The scorer writes `summary.json` and `summary.md`. If no
   non-placeholder submissions exist, it reports `status: incomplete`
   and exits successfully.

## Status discipline

- The audit is **incomplete** until at least one non-placeholder
  submission is scored.
- Do not cite this baseline as "completed" in the paper unless
  `summary.json` reports `n_completed_submissions > 0` and the paper
  explicitly states the completed-submission count.
- `scripts/check_claim_consistency.py` enforces this rule and also
  fails if the task packet is found to leak the canonical estimator or
  L2b+ label.
