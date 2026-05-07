# Submission Build Summary — v11.2-camera-ready

**Build date:** 2026-05-07
**Audit tag:** v11.2-camera-ready
**PDF SHA-256:** `ab8815c83e27175b1a1f5958ab8bc5aa03d1a6130698478ceb4d2d7c6adb72cc`
**PDF size:** 956712 bytes
**Total pages:** 24
**Main body pages:** 9
**References start page:** 10
**Bib entries:** 116 (+2 from v11-freeze: silberzahn2018many, botviniknezer2020variability)

Main content pages before References: 9
References start: page 10
SHA256: `ab8815c83e27175b1a1f5958ab8bc5aa03d1a6130698478ceb4d2d7c6adb72cc`

## Files

- Title: CausalVerify: An Execution-Grounded Benchmark for LLM Causal Inference Workflows
- Source: `paper/latex/causalverify_neurips2026.tex`
- PDF: `paper/latex/causalverify_neurips2026.pdf`
- Style: official NeurIPS 2026 E&D style via `\usepackage[eandd]{neurips_2026}` (anonymous submission mode).

## Lineage

- v11-freeze-2026-04-29 → bib-fix run (transient SHA `802467f3...`, never committed) →
  hardening run (transient SHA `2b25e2f4...`, also never committed) →
  hardening commit (`a1c15edd...`) → Figure 9 colored update →
  **v11.2-camera-ready (final SHA `f71063e3...`)**
- See `audit/sha_trail_investigation.md` for the SHA gap between bib-fix and hardening.

## Changes since v11-freeze

- **Phase 1 derived analyses** (`paper/derived_analyses/`):
  scenario-clustered bootstrap τ CI [0.62, 0.90] (1000/1000 replicates exceed L4 upper bound);
  per-model failure taxonomy (Gemini 63% no-code, Kimi 20% wrong-coef);
  ECE bootstrap CIs (Opus 0.351 [0.288, 0.413] etc.);
  Gemini MCAR check (p=0.877, not rejected);
  tolerance-25 spread (9% to 84%).
- **Tier-1 paper edits (W1/W3/W4/W6/W19):**
  scenario-clustered bootstrap CI in §5 Finding 3;
  Cohen's κ=0.294 hedge lifted into §5 Finding 1;
  L2b+ reframed as agreement with reference implementation;
  Table 7 replaced with per-model breakdown (reconciles to 340 non-L2b+ cells);
  4-LLM consensus pool named (Claude Opus 4.7, GPT-4o, Kimi, Gemini 2.5 Flash);
  structural circularity acknowledged in §3 and §7.
- **Tier-2 polish (10 of 13 applied):**
  Silberzahn 2018 + Botvinik-Nezer 2020 cited (only sanctioned bib changes);
  Llama τ=0.714 honest sentence;
  Event Study n=13 caveat in figure caption;
  tolerance-25 co-headline added to abstract;
  ECE CI note in Figure 8 caption.
  T2.3 footnote inlined (page budget); T2.5 dropped (page budget; stashed in rebuttal kit).
- **Final follow-up:**
  CS=TWFE forward-defense sentence APPLIED in §4 (no compensation trim required);
  T2.5 concurrent-work response stashed in `audit/rebuttal_kit/concurrent_work_response.md`;
  SHA audit trail closed via `audit/sha_trail_investigation.md`.

## Frozen benchmark scope

- Exp A: 259 active papers, 2 quarantined papers, 1813 outputs
  (259 papers × 7 primary models).
- Exp B: 100 synthetic DGP scenarios, 700 primary execution cells
  (100 scenarios × 7 primary models).
- Calibration: 646 valid retrospective self-assessment records.
- Llama-3.3-70B-Instruct retained only as an open-weights Exp B robustness
  check; excluded from the primary seven-model ranking.

## Rebuttal kit (`audit/rebuttal_kit/`)

- `cs_sa_estimator_check.csv` + `.py` — defends W3
  (CS package missing locally, but SA via `fixest::sunab` passes L2b+ on all 3 sampled DIDs at rel-err < 32%)
- `python_replication_plan.md` — defends W7 (n=20 stratified Python replication design)
- `human_baseline_forms/` — defends W5 (10 stratified scenarios, annotation forms ready)
- `concurrent_work_response.md` — defends concurrent-work novelty questions (T2.5 content)

## Frozen-number integrity

All headline numbers preserved:

- L2b+ pass rates 10%–88%
- Kendall τ = 0.81, Spearman ρ = 0.93
- L4 vs L2b+ τ ∈ [−0.20, 0.10]
- Cohen's κ = 0.606 (method) / 0.294 (direction)
- ECE values per `experiments/exp_b/calibration_summary_v2.json` unchanged
- 50-cell coefficient-extraction audit: 90.9% numeric / 88.6% L2b+ pass-fail
- EconCausal N = 10,490 triplets / 2,595 studies

No frozen artifact under `audit/` (except `audit/SUBMISSION_BUILD_SUMMARY.md`,
`audit/sha_trail_investigation.md`, `audit/figure_checks/`, and the new
`audit/rebuttal_kit/`), `experiments/exp_a/outputs/`, or `experiments/exp_b/outputs/`
was modified by this hardening pass.
