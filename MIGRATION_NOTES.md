# MIGRATION_NOTES — figure-style standardization

Scope per the approved plan (Plan A1):

1. Fix legend font/size/position consistency across all 9 figures.
2. Refactor 3 outliers (Fig 1 + 2 orphans) to use `apply_paper_rc()`.
3. Add `paper/figures/regen_all_figs.sh` as the entry point.
4. Verify Fig 5 uses canonical per-model markers (preserve annotations).
5. Visual before/after diff for Fig 3, 4, 5.
6. This file.

Strict NO-OP zones (per constraints): `audit/`, cached LLM outputs,
scoring CSVs, DGP CSVs, figure dimensions, original filenames.

## Single source of truth (unchanged)

`paper/figures/palette.py` remains the canonical style module:

- `apply_paper_rc()` — Arial sans-serif, FONT_AXIS=10, FONT_TICK=9,
  FONT_LEGEND=9, cream `#FAFAFA` background, dotted gray grid,
  black axis lines.
- `MODEL_COLORS` (Wong-Okabe-Ito) and `MODEL_MARKERS` (per-model shape).
- `PAPER_RC` rcParams dict; `AXIS_LABEL_KW` for `set_xlabel/set_ylabel`.

Color and shape mappings are unchanged from the prior unification round.

## Refactored scripts

| Script | Before | After |
|---|---|---|
| `paper/figures/make_fig4_cascade.py` | `FONT_LEGEND = 7` (the user-flagged legend mismatch) | `FONT_LEGEND = 9`, matches Fig 2/3/8. |
| `paper/figures/make_fig_error_cdf.py` (Fig 7) | guide pseudo-legend used `fontsize=8.5/9.5`; per-subplot title `fontsize=13`; suptitle `fontsize=17.5` | guide text → `fontsize=9`; subplot title → `11`; suptitle → `12`. |
| `paper/figures/make_calibration_figures.py` (Fig 8) | per-model subplot title `fontsize=13`; suptitle `fontsize=17` | subplot title → `11`; suptitle → `12`. |
| `paper/figures/make_fig_rid_pilot.py` (Fig 6) | suptitle `fontsize=13.5`; figure-level legend missing explicit `fontsize` | suptitle → `12`; legend `fontsize=9`. |
| `paper/figures/make_fig1_benchmark_construction.py` (Fig 1) | only set `font.family` directly; ignored other paper-wide rcParams | replaced with `apply_paper_rc()`. |
| `paper/figures/make_figure2_headline_v2.py` (orphan) | no `apply_paper_rc()` | added `apply_paper_rc()`. |
| `paper/figures/make_fig_system_flow_v12.py` (orphan) | no `apply_paper_rc()` | added `apply_paper_rc()`. |
| `paper/figures/regen_all_figs.sh` | did not exist | new entry point: regenerate all 9 paper figures from frozen data. |

## NOT refactored (intentional)

- **R / ggplot scripts**: out-of-scope. Repository contains no `library(ggplot2)` use in active paths. The 60+ `audit/human_coder_baseline/submissions/s*.R` files are inside the protected `audit/` zone and contain analyst submissions, not paper figure code.
- **Fig 5 markers**: already used `MODEL_MARKERS[model]` per the previous unification round (verified `paper/figures/make_calibration_gap_scatter.py` line 137). All annotation elements preserved verbatim:
  - Per-model colored text labels
  - Dashed 0% reference line
  - Shaded "weak separation band"
  - Red callout arrow + "high correctness, small confidence gap"
  - "no confidence signal" label
  - `(n=48)` / `(n=99)` suffixes for partial-coverage models.
- **Color/shape remapping**: kept the prior Wong-Okabe-Ito + per-model shape mapping; no change.

## Verification

Side-by-side before/after PNGs saved to `/tmp/legend_diff/`:

- `diff_fig3_method_dotplot.png` — Fig 3 unchanged (was already canonical).
- `diff_fig4_cascade.png` — visible legend-size jump from `FONT_LEGEND=7` → `9`; legend now matches Fig 3.
- `diff_calibration_gap_scatter.png` — Fig 5 unchanged; all annotation
  elements verified preserved.

Page budget unchanged: 24 pages, References on page 10.

## Recompiled artifact

`paper/latex/causalverify_neurips2026.pdf`

- SHA-256: `70b3e740795e566626be94815602120ba653dfb358834b01ed0fd8fe4aec469b`
- Size: 957,110 bytes
- Pages: 24 (main body 9, References p. 10)

## How to re-run

```sh
./paper/figures/regen_all_figs.sh
cd paper/latex && tectonic -X compile causalverify_neurips2026.tex
```
