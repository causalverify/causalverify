#!/usr/bin/env bash
# Regenerate every figure in the paper from frozen data + canonical
# palette.py styling. Run from the repo root:
#
#   ./paper/figures/regen_all_figs.sh
#
# Outputs land in paper/figures/ and paper/latex/figures/. No new LLM API
# calls; deterministic. Uses the canonical paper-wide style defined in
# paper/figures/palette.py (apply_paper_rc + MODEL_STYLE / MODEL_MARKERS).
#
# Active scripts (in figure-number order):
#   1.  make_fig1_benchmark_construction.py    -> fig1_benchmark_construction
#   2.  make_fig2_headline.py                  -> fig2_l2b_plus_cascade
#   3.  make_fig3_clean.py                     -> fig3_method_dotplot
#   4.  make_fig4_cascade.py                   -> fig4_cascade
#   5.  make_calibration_gap_scatter.py        -> calibration_gap_scatter
#   6.  make_fig_rid_pilot.py                  -> fig_rid_pilot
#   7.  make_fig_error_cdf.py                  -> fig_error_cdf
#   8.  make_calibration_figures.py            -> calibration_reliability
#   9.  make_fig_l4_scorer_instability.py      -> fig_l4_scorer_instability
#
# Orphans (not referenced by paper/latex/causalverify_neurips2026.tex):
#   make_figure2_headline_v2.py, make_fig_system_flow_v12.py
# These are skipped here; run them manually if you want to refresh the
# orphan copies.
set -euo pipefail

cd "$(dirname "$0")/../.."

scripts=(
  paper/figures/make_fig1_benchmark_construction.py
  paper/figures/make_fig2_headline.py
  paper/figures/make_fig3_clean.py
  paper/figures/make_fig4_cascade.py
  paper/figures/make_calibration_gap_scatter.py
  paper/figures/make_fig_rid_pilot.py
  paper/figures/make_fig_error_cdf.py
  paper/figures/make_calibration_figures.py
  paper/figures/make_fig_l4_scorer_instability.py
)

for s in "${scripts[@]}"; do
  echo "[regen] $s"
  python3 "$s"
done

echo
echo "All 9 paper figures regenerated."
echo "To recompile the paper: cd paper/latex && tectonic -X compile causalverify_neurips2026.tex"
