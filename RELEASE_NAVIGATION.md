# CausalVerify NeurIPS 2026 Release Navigation

This file is a reviewer-facing map for the final CausalVerify NeurIPS 2026
submission package. Use it to distinguish the submission paper, audit-only
drafts, final result artifacts, and legacy diagnostics.

## Start Here

- Final submission PDF: `paper/latex/causalverify_neurips2026.pdf`
- Final submission source: `paper/latex/causalverify_neurips2026.tex`
- Submission build summary: `audit/SUBMISSION_BUILD_SUMMARY.md`

## Frozen Headline Data

- Scope: Exp A has 259 active papers and 1813 outputs (259 x 7 primary
  models). Exp B has 100 synthetic DGPs and 700 primary execution cells
  (100 x 7 primary models). Calibration has 646 valid records.
- Primary leaderboard scope: seven models only. Llama-3.3-70B-Instruct is
  retained as an open-weights Exp B robustness check, not included in
  `head_to_head_ranking.json`.
- Exp A text-level scores: `experiments/exp_a/auto_scores.csv`
- Exp A model table: `paper/tables/exp_a_l3_l4_by_model.csv`
- Exp B realised CSV datasets (100 scenarios, one CSV per scenario):
  `experiments/exp_b/data/s*_data.csv`
- Exp B scenario metadata (100 scenario JSONs, one per scenario):
  `experiments/exp_b/scenarios/s*.json`
- Exp B canonical-estimator targets and L2b+ scoring outputs:
  `experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv` (per-cell
  rows include `canonical_estimate`, `judge_effect`, `rel_error_v2`,
  `L2b_plus_v2`)
- Exp B L2b+ scores: `experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv`
  (7 primary models plus Llama robustness rows)
- Exp B L2b+ summary: `experiments/exp_b/l2b_plus_summary_canonical_judge_v2.json`
  (7 primary models plus Llama robustness entry)
- L2b/L2b+ ranking analysis: `experiments/exp_b/head_to_head_ranking.json`
- Calibration summary: `experiments/exp_b/calibration_summary_v2.json`
- Human-gold validation audit: `audit/human_gold/human_vs_llm_consensus.md`
- Exp B Dataset URL: `https://huggingface.co/datasets/causalverify/causalverify-neurips2026`
- Exp B Croissant metadata: `experiments/exp_b/croissant.json`

## Exp B Robustness Audit

- Audit overview: `audit/exp_b_robustness/README.md`
- Conditional L2b table: `paper/tables/exp_b_l2b_conditional_primary7.csv`
- Scorer evolution table: `paper/tables/exp_b_scorer_evolution_primary7.csv`
- Method-family breakdown: `paper/tables/exp_b_l2bplus_by_model_method_primary7.csv`
- Tolerance sweep: `paper/tables/exp_b_tolerance_sweep_primary7.csv`

## L2b Judge Human-Validation Audit

- Protocol overview: `audit/l2b_judge_human_validation/README.md`
- Blinded annotation form: `audit/l2b_judge_human_validation/annotation_form.csv`
- Completed summary: `audit/l2b_judge_human_validation/summary.md`
- Preparation script: `scripts/prepare_l2b_judge_human_validation.py`
- Summary script: `scripts/summarize_l2b_judge_human_validation.py`
- Result: a blinded 50-cell audit of primary-panel L2b=1 executions found
  90.9% numeric agreement and 88.6% induced L2b+ pass/fail agreement among
  comparable audited cells. Disagreements concentrate in event-study window
  choices and RDD sign/printing ambiguities.
- The hidden unblinding key (`annotation_key_private.csv`) is **intentionally
  withheld from this anonymous release** because it contains unblinding
  metadata (model identity, canonical estimates, judge effects, and L2b+
  labels). Reviewers should consult `summary.md` and `summary.json` for the
  completed audit results; the `summarize` script gracefully reports the
  withheld-key case and exits with status 0.

## Figures

- Figure 2: `paper/figures/fig2_l2b_plus_cascade.pdf`
- Figure 3: `paper/figures/fig3_method_dotplot.pdf`
- Figure 4: `paper/figures/fig4_cascade.pdf`
- Figure 5: `paper/figures/fig_error_cdf.pdf`
- Calibration reliability: `paper/figures/calibration_reliability.pdf`
- Calibration gap scatter: `paper/figures/calibration_gap_scatter.pdf`
- RID pilot appendix: `paper/figures/fig_rid_pilot.pdf`

## Reproduce Without New LLM Calls

```bash
python src/pipeline/auto_score_exp_a.py
python src/pipeline/score_l2b_plus.py --baseline canonical
python scripts/l2b_llm_judge_extract.py --all --cache-only
python scripts/recompute_l2b_plus_es_aware.py
python src/pipeline/head_to_head_ranking.py
python paper/figures/make_fig2_headline.py
python paper/figures/make_fig3_clean.py
python paper/figures/make_fig4_cascade.py
python paper/figures/make_fig_error_cdf.py
python paper/figures/make_calibration_figures.py
```

The `--cache-only` flag on `l2b_llm_judge_extract.py` verifies coverage
against the frozen `audit/l2b_judge_cache.json` and refuses to
instantiate the Anthropic client; fresh judge extraction (without that
flag) may require API calls and is therefore outside the no-new-LLM
path.

## Legacy Artifacts

The repository keeps older artifacts for auditability. They should not be
used for the headline benchmark claims unless explicitly labeled in the paper.

- `legacy/evaluate_v1_causalbench.py`: pre-CausalVerify CAUSAL-BENCH-era
  evaluator. Audit-only; replaced by the dispatcher at `evaluate.py` and
  the scoring scripts under `src/pipeline/` and `scripts/`.
- `experiments/exp_a/outputs_v1_legacy/`: Exp A outputs from before the
  final paper-field reconstruction pass.
- `experiments/exp_a/auto_scores_v1_legacy.csv`: Exp A scores from before
  the final paper-field reconstruction pass.
- `experiments/exp_b/l2b_plus_scores.csv`: regex-era L2b+ diagnostic.
- `experiments/exp_b/head_to_head_bootstrap.json`: legacy diagnostic bootstrap.

The frozen headline numbers are the files listed under "Frozen Headline Data"
above.
