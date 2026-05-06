# Human Coder Baseline — Task Packet

You will receive 20 blinded Exp B scenarios stratified across DID, Event
Study, IV, and RDD. Each scenario lives in its own ``{sid}_task.md``
file in this directory.

## Your task

For each scenario:

1. Read ``{sid}_task.md``. It contains the research question, the data
   description, the path to a CSV file, a preview of that file, and the
   column types. This is the **same** information the evaluated LLMs
   received.

2. Write a standalone R script that:
   - reads the CSV from the path printed in the task,
   - implements the appropriate causal-inference design,
   - prints the treatment-effect estimate in EXACTLY this format on its
     own line:

     ```r
     cat("treatment_effect_estimate:", estimate, "\n")
     ```

3. Save the script as
   ``audit/human_coder_baseline/submissions/{sid}_submission.R``.

## What you do NOT see

Per the blinding protocol you do NOT see the canonical estimator's
output, the L2b+ pass label, the DGP parameter ``dgp_truth.effect``, the
LLM model outputs, or any judge output. Do not look these up before
finishing your submissions.

## What this baseline measures

This is a **solvability audit**. A submission is L2b-correct if your R
script executes without error; it is L2b+-correct if your printed
``treatment_effect_estimate`` matches the canonical estimator on the
realised dataset within the same tolerance the paper uses (relative
error ≤ 50 %, with ES-window-aware acceptance for Event Study). The
audit is *not* a population estimate of expert performance.
