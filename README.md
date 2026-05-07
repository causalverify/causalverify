<h1 align="center">CausalVerify</h1>

<p align="center">
  <b>CausalVerify: An Execution-Grounded Benchmark for LLM Causal Inference Workflows</b><br>
  <sub>An execution-grounded benchmark for causal-inference workflows.</sub>
</p>

<p align="center">
  <!-- CI badge removed for anonymous review; will be restored on acceptance -->
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/Code-MIT-blue.svg"></a>
  <a href="LICENSE_DATA.md"><img alt="Data license notes" src="https://img.shields.io/badge/Data-component--level-lightgrey.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-green.svg">
  <img alt="R" src="https://img.shields.io/badge/R-4.4.2-blueviolet.svg">
</p>

---

## Frozen submission state

Both the dataset and code releases are pinned with the stable tag
`neurips2026-submission`. Reviewers should evaluate against the tag URLs
below; updates to `main` after the deadline are documentation or
clarification only.

- **Dataset:** [`causalverify/causalverify-neurips2026`](https://huggingface.co/datasets/causalverify/causalverify-neurips2026/tree/neurips2026-submission)
  at tag `neurips2026-submission`. Contents: 100 fixed-seed Exp B
  scenarios, 100 realised CSV datasets, 800 cached LLM outputs (8 models
  × 100 scenarios), frozen scoring CSV/JSON, datasheet, Croissant
  metadata.
- **Code:** [`causalverify/causalverify-code-neurips2026`](https://huggingface.co/datasets/causalverify/causalverify-code-neurips2026/tree/neurips2026-submission)
  at tag `neurips2026-submission`. Mirrors this repository at the
  submission commit, identity-cleaned (no institution-specific fetchers,
  no internal session notes, anonymous LICENSE).
- **Anonymous code mirror:** [`anonymous.4open.science/r/causalverify-1B47/`](https://anonymous.4open.science/r/causalverify-1B47/)
  auto-syncs from this repository's `main`.

---

## Reviewer quick map

- Final submission paper: [`paper/latex/causalverify_neurips2026.pdf`](paper/latex/causalverify_neurips2026.pdf), source [`paper/latex/causalverify_neurips2026.tex`](paper/latex/causalverify_neurips2026.tex).
- Submission build summary: [`audit/SUBMISSION_BUILD_SUMMARY.md`](audit/SUBMISSION_BUILD_SUMMARY.md).
- Frozen result gates: [`audit/V11_ACCEPTANCE_GATES.md`](audit/V11_ACCEPTANCE_GATES.md).
- Human validation audit: [`audit/human_gold/human_vs_llm_consensus.md`](audit/human_gold/human_vs_llm_consensus.md).
- Release navigation for reviewers: [`RELEASE_NAVIGATION.md`](RELEASE_NAVIGATION.md).
- Datasheet and licensing: [`DATASHEET.md`](DATASHEET.md), [`LICENSE_DATA.md`](LICENSE_DATA.md).
- Exp B dataset URL: https://huggingface.co/datasets/causalverify/causalverify-neurips2026
- Exp B Croissant metadata: [`experiments/exp_b/croissant.json`](experiments/exp_b/croissant.json).

Frozen scope: Exp A has 259 active papers and 1813 outputs (259 x 7 primary
models); Exp B has 100 synthetic DGPs and 700 primary execution cells
(100 x 7 primary models); calibration has 646 valid records.
The primary leaderboard uses seven models. Llama-3.3-70B-Instruct is retained
only as an open-weights robustness check in Exp B artifacts and is excluded
from the primary Kendall/Spearman ranking.

## Why CausalVerify

When LLMs are used to produce policy-relevant causal estimates, who verifies that the model's code actually computes the right number? Existing causal-inference benchmarks answer this through **text inspection**: they read what the model *says* and check it against a text-based answer key. We argue that this is insufficient: *a benchmark of language is not the same as a benchmark of computation*. Executable code is not necessarily causally correct, and only **execution-grounded evaluation** can detect that gap.

CausalVerify is a benchmark of **259 active published economics papers** (Experiment A; two papers quarantined: one for OCR-corrupt source, one for PDF/metadata mismatch) and **100 synthetic data-generating processes** (Experiment B) for evaluating LLM causal-inference workflows across frontier models. Its central methodological contribution is **L2b+**, an execution-grounded scoring layer that runs each model's generated R code against synthetic data and verifies that the estimated treatment effect matches the **canonical estimator on the realised dataset**. This avoids penalizing models for finite-sample deviations between the realised dataset and the ideal DGP parameter.

### Headline results (Experiment B, N = 100 DGPs)

| Statement | Evidence |
|---|---|
| L2b (code executes) ranks models tightly with L2b+ correctness | Kendall τ = +0.81; Spearman ρ = +0.93 across 7 models |
| L4 agreement against consensus direction labels does not track Exp B L2b+ ranking | τ ∈ [−0.20, +0.10] across the frozen S1/S2 text-direction scorers |
| Code that runs is not code that computes correctly | L2b rates span 32–94%; final ES-aware canonical L2b+ spans 10–88% (GPT-5 ranks second at 72%) |
| The coefficient extractor is validated, not regex-only | Regex L2b+ is retained as legacy; v11 uses Haiku extraction + ES-aware canonical scoring |
| Text-level scores are supporting diagnostics | L3/L4 are method-family and direction agreement diagnostics, not verified causal correctness |

---

## The layered evaluation framework

| Layer | Question | Scoring | Requires DGP |
|---|---|---|---|
| **L1** | Output is non-empty? | Deterministic (length) | No |
| **L2a** | Contains R code block? | Deterministic (regex) | No |
| **L2b** | Code executes without error? | Deterministic (`Rscript`) | No |
| **L2b+** | Estimated coefficient matches canonical estimator? | Execution + judge extraction + numeric check | **Yes** |
| **L3** | Method-family agreement (text-level)? | Text-inspection, fragile | No |
| **L4** | Direction agreement (text-level)? | Text-inspection, fragile | No |

L2b+ is the only layer that combines executed code with a numeric correctness check against a canonical estimator. It is computable only on Experiment B. Experiment A contributes ecological breadth and text-level agreement diagnostics.

---

## Repository layout

```text
CAUSALVERIFY/
├── paper/                              # the NeurIPS submission
│   ├── latex/
│   │   ├── causalverify_neurips2026.tex # final submission source
│   │   ├── causalverify_neurips2026.pdf # final submission output
│   │   ├── references.bib              # bibliography
│   │   └── checklist.tex               # NeurIPS paper checklist
│   └── figures/
│       ├── palette.py                  # canonical colors + font settings
│       ├── make_fig2_headline.py       # Figure 2 (three-panel headline)
│       ├── make_fig3_clean.py          # Figure 3 (L3 method dotplot)
│       ├── make_fig4_cascade.py        # Figure 4 (execution cascade)
│       ├── make_fig_error_cdf.py       # Figure 5 (L2b+ error profiles)
│       ├── make_fig_rid_pilot.py       # RID pilot figure
│       └── *.pdf, *.png                # rendered figures
│
├── experiments/                        # benchmark data + scored outputs
│   ├── exp_a/                          # Experiment A — 259 active real papers
│   │   ├── papers/                     # local/reviewer-only source files; not public CC BY data
│   │   ├── outputs/                    # per-model responses
│   │   ├── ground_truth_extractions/   # extracted causal claims
│   │   ├── human_ratings/              # legacy ratings; final audit is in audit/human_gold/
│   │   ├── llm_ratings/                # LLM rater outputs
│   │   ├── multi_scorer_cache/         # S1–S4 scorer intermediates
│   │   ├── auto_scores.csv             # L1/L2a/L2b/L3/L4 scores
│   │   └── multi_scorer_l4.csv         # L4 fragility analysis
│   ├── exp_b/                          # Experiment B — 100 synthetic DGPs
│   │   ├── scenarios/                  # scenario JSON specifications
│   │   ├── data/                       # synthetic CSV per scenario
│   │   ├── outputs/                    # per-model responses
│   │   ├── l2b_plus_scores_canonical_judge_v2.csv   # frozen L2b+ scores
│   │   ├── l2b_plus_summary_canonical_judge_v2.json # frozen per-model rates
│   │   ├── head_to_head_ranking.json   # frozen 7-model Kendall τ / Spearman analysis
│   │   └── head_to_head_bootstrap.json # legacy diagnostic bootstrap artifact
│   ├── exp_c_v2/                       # RID ablation pilot (N=10 per model)
│   └── prompt_sensitivity/             # V0 vs V1 method-name ablation
│
├── src/
│   ├── pipeline/                       # end-to-end pipeline scripts
│   │   ├── run_exp_a.py                # run Experiment A on a model
│   │   ├── run_exp_b.py                # run Experiment B on a model
│   │   ├── run_exp_c_v2.py             # run RID ablation pilot
│   │   ├── run_prompt_sensitivity.py   # run V0/V1 ablation
│   │   ├── score_exp_a.py              # Experiment A scoring
│   │   ├── auto_score_exp_a.py         # L1/L2a/L2b/L3/L4 automation
│   │   ├── score_exp_b.py              # Experiment B scoring
│   │   ├── score_l2b_plus.py           # L2b+ coefficient verification
│   │   ├── head_to_head_ranking.py     # Kendall τ ranking analysis
│   │   ├── bootstrap_head_to_head.py   # bootstrap CI for τ
│   │   ├── multi_scorer_l4.py          # S1–S4 L4 scorer fragility
│   │   ├── generate_exp_b_scenarios.py # scenario generator
│   │   └── extend_exp_b_to_100.py      # scenario expansion
│   ├── evaluation/                     # validity checklists
│   ├── prompts/                        # prompt templates
│   ├── rid/                            # research-integrity discipline module
│   ├── connectors/                     # provider SDK wrappers
│   ├── analysis/                       # post-hoc analyses
│   └── llm_client.py                   # unified LLM client
│
├── evaluate.py                         # safe dispatcher to current scoring scripts
├── legacy/                             # audit-only: pre-CausalVerify CAUSAL-BENCH evaluator
├── requirements.txt                    # Python dependencies
├── config.yaml                         # global configuration
├── sample.env                          # API key template
├── DATASHEET.md                        # NeurIPS D&B datasheet
├── LICENSE_DATA.md                     # component-level data/license notes
├── LICENSE
└── README.md
```

---

## Quick start

### 1. Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. R environment (required for L2b / L2b+)

L2b and L2b+ run the model-generated R code through `Rscript --vanilla`. Install R and the packages used across the benchmark:

```r
install.packages(c("fixest", "AER", "rdrobust", "sandwich",
                   "lmtest", "dplyr", "data.table"))
```

### 3. API keys

Copy the template and fill in your provider keys:

```bash
cp sample.env .env
# edit .env with OPENAI_API_KEY, ANTHROPIC_API_KEY,
#                GOOGLE_API_KEY, MOONSHOT_API_KEY
```

---

## Reproducing frozen submission results

All model outputs and scored data are already in `experiments/`. The commands below re-run scoring and ranking **without any new LLM calls**.

### Re-score Experiment A (L1, L2a, L2b, L3, L4)

```bash
python src/pipeline/auto_score_exp_a.py
```

Produces `experiments/exp_a/auto_scores.csv`.

### Re-score Experiment B and run the L2b+ analysis

```bash
python src/pipeline/score_l2b_plus.py --baseline canonical
python scripts/l2b_llm_judge_extract.py --all --cache-only
python scripts/recompute_l2b_plus_es_aware.py
python src/pipeline/head_to_head_ranking.py
python src/pipeline/bootstrap_head_to_head.py
```

The frozen release includes the L2b judge cache
(`audit/l2b_judge_cache.json`). Deterministic reproduction consumes cached
judge outputs only; the `--cache-only` flag verifies coverage and refuses
to instantiate the Anthropic client. Running judge extraction from
scratch (without `--cache-only`) may require API calls and is not part of
the no-new-LLM path.

Coefficient-extraction judge validation is documented in
`audit/l2b_judge_human_validation/`: a blinded 50-cell audit of primary-panel
L2b=1 executions found 90.9% numeric agreement and 88.6% induced L2b+
pass/fail agreement among comparable audited cells. Disagreements concentrate
in event-study window choices and RDD sign/printing ambiguities.

Final submission reporting uses `experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv` and `l2b_plus_summary_canonical_judge_v2.json`. Regex-only outputs are retained as legacy diagnostics, not as paper headline numbers.
These L2b+ files also retain Llama-3.3-70B-Instruct rows for the open-weights
robustness check. The primary leaderboard and `head_to_head_ranking.json`
exclude Llama and report the seven-model panel only.

### Multi-scorer L4 fragility analysis

```bash
python src/pipeline/multi_scorer_l4.py
```

Produces `experiments/exp_a/multi_scorer_l4.csv` (S1 latter-half, S2 section-aware, S3 LLM-as-judge, S4 structured JSON).

### Regenerate all paper figures

```bash
python paper/figures/make_fig2_headline.py     # Figure 2 (headline)
python paper/figures/make_fig3_clean.py        # Figure 3 (L3 dotplot)
python paper/figures/make_fig4_cascade.py      # Figure 4 (cascade)
python paper/figures/make_fig_error_cdf.py     # Figure 5 (error profiles)
python paper/figures/make_fig_rid_pilot.py     # RID pilot figure
```

All figures share a canonical font/color stack via `paper/figures/palette.py`.

### Check frozen claim consistency

```bash
python scripts/check_claim_consistency.py
```

This check scans reviewer-facing docs for stale v10/v11-era numbers and
verifies that release-navigation artifact paths exist.

### Security note for new R-code execution

L2b and L2b+ execute model-generated R code. Run new, unfrozen model outputs
only inside the provided Docker container, with no API keys mounted and
preferably with network disabled.

### Build the paper

Via local TeX Live:

```bash
cd paper/latex
pdflatex -interaction=nonstopmode causalverify_neurips2026.tex
bibtex causalverify_neurips2026
pdflatex -interaction=nonstopmode causalverify_neurips2026.tex
pdflatex -interaction=nonstopmode causalverify_neurips2026.tex
```

Or via Docker (no local LaTeX install required):

```bash
docker run --rm -v $(pwd)/paper:/paper -w /paper/latex \
  texlive/texlive:latest bash -c "
    pdflatex -interaction=nonstopmode causalverify_neurips2026.tex &&
    bibtex  causalverify_neurips2026 &&
    pdflatex -interaction=nonstopmode causalverify_neurips2026.tex &&
    pdflatex -interaction=nonstopmode causalverify_neurips2026.tex"
```

---

## Running new experiments

### Experiment A: run the benchmark on a new model

```bash
python src/pipeline/run_exp_a.py --all --model gpt-4o
```

### Experiment B: 100 DGP-grounded scenarios

```bash
python src/pipeline/run_exp_b.py --all --model gpt-4o
python src/pipeline/score_l2b_plus.py
```

### Experiment C v2: RID ablation pilot

```bash
python src/pipeline/run_exp_c_v2.py --report
```

### Prompt sensitivity (V0 vs V1 method-name ablation)

```bash
python src/pipeline/run_prompt_sensitivity.py
```

### Generate new Experiment B scenarios from scratch

```bash
python src/pipeline/generate_exp_b_scenarios.py
python src/pipeline/extend_exp_b_to_100.py
```

---

## Paper navigation

The paper structure mirrors the repository layout:

| Paper section | Code / data location |
|---|---|
| §1 Introduction | [`paper/latex/causalverify_neurips2026.tex`](paper/latex/causalverify_neurips2026.tex) |
| §2 Related Work and Positioning | [`paper/latex/causalverify_neurips2026.tex`](paper/latex/causalverify_neurips2026.tex) |
| §3 Benchmark Design | [`src/agents/`](src/agents/), [`experiments_log/decisions/`](experiments_log/decisions/) |
| §4 Evaluation Layers | [`src/pipeline/score_l2b_plus.py`](src/pipeline/score_l2b_plus.py), [`src/pipeline/auto_score_exp_a.py`](src/pipeline/auto_score_exp_a.py) |
| §5 Findings (R1–R5) | [`experiments/exp_b/head_to_head_ranking.json`](experiments/exp_b/head_to_head_ranking.json), [`paper/tables/exp_a_l3_l4_by_model.csv`](paper/tables/exp_a_l3_l4_by_model.csv) |
| §5 Experiment A — 259 papers | [`experiments/exp_a/`](experiments/exp_a/), [`experiments/exp_a/auto_scores.csv`](experiments/exp_a/auto_scores.csv) |
| §5 Experiment B — 100 DGPs | [`experiments/exp_b/`](experiments/exp_b/), [`experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv`](experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv) |
| Human validation audit — 30 papers | [`audit/human_gold/paper_native_labels.csv`](audit/human_gold/paper_native_labels.csv), [`audit/human_gold/human_vs_llm_consensus.md`](audit/human_gold/human_vs_llm_consensus.md) |
| F4 — L4-text multi-scorer fragility | [`src/pipeline/multi_scorer_l4.py`](src/pipeline/multi_scorer_l4.py), [`experiments/exp_a/multi_scorer_l4.csv`](experiments/exp_a/multi_scorer_l4.csv) |
| Prompt sensitivity | [`experiments/prompt_sensitivity/`](experiments/prompt_sensitivity/) |
| §8 Limitations | [`paper/latex/causalverify_neurips2026.tex`](paper/latex/causalverify_neurips2026.tex) |
| §9 Conclusion | [`paper/latex/causalverify_neurips2026.tex`](paper/latex/causalverify_neurips2026.tex) |
| Appendix A — F5 support | [`experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv`](experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv) |
| Repository artifact — L3/L4 heatmap | [`paper/figures/replication_heatmap.png`](paper/figures/replication_heatmap.png) |
| Appendix — RID ablation pilot | [`paper/figures/fig_rid_pilot.pdf`](paper/figures/fig_rid_pilot.pdf), [`experiments/exp_c_v2/`](experiments/exp_c_v2/), [`src/pipeline/run_exp_c_v2.py`](src/pipeline/run_exp_c_v2.py) |
| Appendix D — Error case studies | [`experiments/exp_a/outputs/`](experiments/exp_a/outputs/) |

---

## Models evaluated

| Model | Provider | Identifier |
|---|---|---|
| Claude Opus | Anthropic | `claude-opus-4-6` |
| Claude Sonnet | Anthropic | `claude-sonnet-4-20250514` |
| GPT-4o | OpenAI | `gpt-4o` |
| o3 | OpenAI | `o3` |
| GPT-5 | OpenAI | `gpt-5` |
| Kimi | Moonshot | `moonshot-v1-128k` |
| Gemini 2.5 Flash | Google | `gemini-2.5-flash` |

> Gemini responses are truncation-limited in parts of the benchmark, especially calibration. The frozen tables report Gemini where available and mark incomplete calibration coverage explicitly.

---

## Citation

```bibtex
@inproceedings{anon2026causalverify,
  title  = {CausalVerify: An Execution-Grounded Benchmark for LLM Causal Inference Workflows},
  author = {Anonymous},
  year   = {2026},
  note   = {Under review at NeurIPS 2026 Evaluations \& Datasets Track; author identity withheld for double-blind review.}
}
```

---

## License

| Component | License |
|---|---|
| Code | MIT — see [`LICENSE`](LICENSE) |
| Data (scenarios, scored outputs, summaries) | CC BY 4.0 |
| Benchmark documentation | See [`DATASHEET.md`](DATASHEET.md) |
