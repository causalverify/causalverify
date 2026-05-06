# CausalVerify NeurIPS 2026 submission build summary

Date: 2026-05-06

Purpose: record the final anonymous CausalVerify NeurIPS 2026 Evaluations &
Datasets submission build. This file replaces the prior internal draft
summary and should be treated as the reviewer-facing paper build record.

## Files

- Title: CausalVerify: An Execution-Grounded Benchmark for LLM Causal Inference Workflows
- Source: `paper/latex/causalverify_neurips2026.tex`
- PDF: `paper/latex/causalverify_neurips2026.pdf`
- Style: official NeurIPS 2026 E&D style via
  `\usepackage[eandd]{neurips_2026}` (anonymous submission mode).
- SHA256: `eaff2475f2f73e747b97d85738b76cf6ede7742de5290a09b64dcb6fc051f78a`
- Size: 934846 bytes

## Frozen benchmark scope

- Exp A: 259 active papers, 2 quarantined papers, 1813 outputs
  (259 papers x 7 primary models).
- Exp B: 100 synthetic DGP scenarios, 700 primary execution cells
  (100 scenarios x 7 primary models).
- Calibration: 646 valid retrospective self-assessment records.
- Llama-3.3-70B-Instruct is retained only as an open-weights Exp B robustness
  check and is excluded from the primary seven-model ranking.

## Page budget

The NeurIPS 2026 main-track / E&D-track formatting rule limits the main
content to 9 pages; references, appendices, and checklist do not count as
content pages.

Current final-submission layout, revalidated under the official NeurIPS 2026
E&D style:

- Total PDF pages: 21
- Main content pages before References: 9
- References start: page 10
- Appendix starts: page 14
- Checklist starts: page 19

The main text now satisfies the 9-page limit under the official NeurIPS 2026
E&D style. Detailed reproducibility, human-audit material, the RID pilot, and
additional diagnostic figures are placed in the appendix so the main text
remains within the submission budget.

Local validation command:

```bash
cd paper/latex
tectonic -X compile causalverify_neurips2026.tex --outdir /tmp/causalverify_neurips2026_build --keep-logs
```

The compile completed successfully with layout warnings only (underfull boxes
and a `lineno.sty` UTF-8 warning), not fatal errors.

## Submission source

- `paper/latex/causalverify_neurips2026.tex` and
  `paper/latex/causalverify_neurips2026.pdf` are the only submission source
  and PDF. Earlier internal drafts (`neurips_v10*`, `neurips_v11*`,
  `neurips_v12*`) were removed; the pre-restructure state remains accessible
  via the git tag `pre-v2prime-restructure-2026-04-25`.

## Human-validation status

The 30-paper blinded Exp A human validation audit is completed:

- Target30 completed: 30/30 first-pass human labels.
- Replacement: `paper_159` was excluded because the available PDF was
  appendix-only; `paper_17` was added as a blinded replacement.
- Human vs 4-LLM consensus:
  - Method-family agreement: 18/30 = 60.0% (Cohen's kappa 0.606).
  - Direction agreement: 10/21 = 47.6% (Cohen's kappa 0.294).
- Source: `audit/human_gold/human_vs_llm_consensus.md`.

This audit bounds Exp A label ambiguity. It does not make the full Exp A
corpus human-gold labeled.

The L2b coefficient-judge human-validation audit is completed:

- Protocol: `audit/l2b_judge_human_validation/README.md`
- Current summary: `audit/l2b_judge_human_validation/summary.json`
- Scope: 50 primary-panel L2b=1 cells sampled with seed 20260502.
- Result: 90.9% numeric agreement and 88.6% induced L2b+ pass/fail
  agreement among comparable audited cells.
- Disagreements concentrate in event-study window choices and RDD
  sign/printing ambiguities.

## Claim-boundary reminders

- L2b+ means coefficient agreement with the canonical estimator on the
  realised dataset, not recovery of the ideal DGP beta parameter.
- L3/L4 are text-level method-family and direction agreement diagnostics, not
  verified causal correctness.
- The primary leaderboard has seven models; Llama remains robustness-only.
