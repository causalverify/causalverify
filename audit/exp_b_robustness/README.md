# Exp B Robustness Audit

This audit strengthens the interpretation of Exp B without replacing the
frozen headline L2b+ artifacts. It is derived from
`experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv` and does not
make LLM API calls or regenerate model outputs.

## Interpretation

- L2b+ requires L2b, so a raw association between L2b and L2b+ is partly
  structural: code must execute before a coefficient can be checked.
- The conditional metric `P(L2b+ v2 | L2b)` asks a sharper question:
  among outputs whose code executed, how often did the workflow compute
  the canonical treatment-effect estimate on the realised dataset?
- The n=7 rank correlations are descriptive diagnostics over the frozen
  primary model panel, not population-level claims about all possible LLMs.
- Leave-one-model-out rank stability is reported to show sensitivity to
  model-panel composition.
- Primary-7 results are kept separate from Llama. Llama-3.3-70B-Instruct
  is retained only as an open-weights robustness check and is not part of
  the primary 7-model Kendall/Spearman ranking.
- L2b+ means coefficient agreement with the canonical estimator on the
  realised dataset, not recovery of the ideal DGP beta parameter.
- The tolerance sweep is an all-scenario diagnostic over the primary seven
  models. It reports alternative relative-error cutoffs while keeping the
  frozen headline endpoint at the default 50% tolerance.

## Rank-Stability Diagnostic

The primary seven-model L2b-vs-L2b+ rank diagnostic is unchanged:
Kendall tau is 0.8095 and Spearman rho is 0.9286. Leave-one-model-out
diagnostics keep the Kendall tau range between 0.7333 and 0.8667
(mean 0.8095) and the Spearman rho range between 0.8857 and 0.9429
(mean 0.9184). A separate `primary 7 plus Llama robustness-only`
diagnostic gives Kendall tau 0.7143 and Spearman rho 0.8810. This
Llama-inclusion diagnostic is not part of the primary leaderboard and
is not written to `experiments/exp_b/head_to_head_ranking.json`.

## Tolerance-Sweep Diagnostic

The W2 tolerance sweep recomputes primary-seven all-scenario L2b+ pass rates
at 10%, 25%, 50%, 75%, and 100% relative-error cutoffs. The denominator is
100 Exp B scenarios per model; non-executing outputs remain failures. At the
default 50% tolerance, the sweep exactly reproduces the frozen headline L2b+
counts. At 25% tolerance, the top three primary models remain above the
remaining four, and Gemini/Kimi remain the bottom two.

## Primary-7 Conditional L2b Table

| Model | n | L2b | L2b+ v2 | Executed but not correct | P(L2b+ v2 given L2b) |
|---|---:|---:|---:|---:|---:|
| Kimi | 100 | 45 (0.45) | 10 (0.10) | 35 | 0.22 |
| Sonnet | 100 | 51 (0.51) | 50 (0.50) | 1 | 0.98 |
| GPT-4o | 100 | 78 (0.78) | 62 (0.62) | 16 | 0.79 |
| o3 | 100 | 50 (0.50) | 46 (0.46) | 4 | 0.92 |
| Opus | 100 | 94 (0.94) | 88 (0.88) | 6 | 0.94 |
| Gemini | 100 | 32 (0.32) | 32 (0.32) | 0 | 1.00 |
| GPT-5 | 100 | 76 (0.76) | 72 (0.72) | 4 | 0.95 |

## Llama Robustness-Only Result

| Model | n | L2b | L2b+ v2 | Executed but not correct | P(L2b+ v2 given L2b) |
|---|---:|---:|---:|---:|---:|
| Llama | 100 | 41 (0.41) | 20 (0.20) | 21 | 0.49 |

## Generated Files

- `paper/tables/exp_b_l2b_conditional_primary7.csv`
- `paper/tables/exp_b_rank_stability_primary7.csv`
- `paper/tables/exp_b_scorer_evolution_primary7.csv`
- `paper/tables/exp_b_l2bplus_by_model_method_primary7.csv`
- `paper/tables/exp_b_tolerance_sweep_primary7.csv`
- `audit/exp_b_robustness/l2b_conditional_primary7.json`
- `audit/exp_b_robustness/l2b_conditional_llama_robustness.json`
- `audit/exp_b_robustness/rank_stability_primary7.csv`
- `audit/exp_b_robustness/rank_stability_primary7.json`
- `audit/exp_b_robustness/scorer_evolution_primary7.json`
- `audit/exp_b_robustness/l2bplus_by_model_method_primary7.json`
- `audit/exp_b_robustness/tolerance_sweep_primary7.csv`
- `audit/exp_b_robustness/tolerance_sweep_primary7.json`
