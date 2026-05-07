"""Generate preview Figure 2: headline CausalVerify results.

Outputs:
  paper/figures/figure2_headline_v2.pdf
  paper/figures/figure2_headline_v2.png

This preview reads frozen result artifacts only and makes no model/API calls.
It does not replace the LaTeX figure until explicitly requested.
"""

from __future__ import annotations

import json
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from palette import apply_paper_rc
apply_paper_rc()

from cv_style import (
    COLORS,
    MODEL_COLORS,
    MODEL_ORDER,
    clean_axis,
    percent_axis,
    set_cv_style,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "paper/figures"


def load_json(path: str):
    return json.loads((ROOT / path).read_text())


def load_exp_a_table():
    path = ROOT / "paper/tables/exp_a_l3_l4_by_model.csv"
    name_map = {
        "Claude-Opus": "Opus",
        "Claude-Sonnet": "Sonnet",
        "Kimi-128k": "Kimi",
        "Gemini-2.5": "Gemini",
    }
    rows = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            model = name_map.get(row["model"], row["model"])
            rows[model] = {
                "L3": float(row["L3_pct"]),
                "L4": float(row["L4_pct"]),
            }
    return rows


def panel_execution_gap(ax, canonical, v2):
    models = [m for m in MODEL_ORDER if m in canonical["by_model"] and m in v2["by_model"]]
    y = np.arange(len(models))
    l2b = np.array([canonical["by_model"][m]["L2b_rate"] * 100 for m in models])
    l2bp = np.array([v2["by_model"][m]["L2b_plus_v2_rate"] * 100 for m in models])

    ax.barh(y, l2bp, height=0.42, color=COLORS["correct"], edgecolor="none", zorder=2)
    for yi, model, executed, correct in zip(y, models, l2b, l2bp):
        ax.plot([correct, executed], [yi, yi], color=COLORS["gap"], linewidth=2.2,
                solid_capstyle="round", zorder=1)
        ax.scatter(
            executed, yi,
            marker="o",
            s=30,
            color=COLORS["exec"],
            edgecolor="white",
            linewidth=0.45,
            zorder=4,
        )
        if correct >= 20:
            ax.text(correct - 1.5, yi, f"{correct:.0f}%", ha="right", va="center",
                    fontsize=7.0, color="white", fontweight="bold")
        else:
            ax.text(correct + 1.6, yi, f"{correct:.0f}%", ha="left", va="center",
                    fontsize=7.0, color=COLORS["ink"], fontweight="bold")
        gap = executed - correct
        if model == "Kimi":
            ax.text(executed + 1.8, yi, f"{gap:.0f}pp", ha="left", va="center",
                    fontsize=7.0, color=COLORS["muted"])

    ax.set_yticks(y)
    ax.set_yticklabels(models)
    ax.invert_yaxis()
    percent_axis(ax, "x")
    clean_axis(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Share of Exp B scenarios (%)", fontsize=7.6, labelpad=6)
    ax.set_title("(a) Execution vs. coefficient correctness",
                 loc="left", pad=3, fontsize=8.2)

    handles = [
        Line2D([0], [0], color=COLORS["correct"], lw=4.2,
               solid_capstyle="butt", label="L2b+ correct"),
        Line2D([0], [0], marker="o", color="white", markerfacecolor=COLORS["exec"],
               markeredgecolor="white", markersize=5, label="L2b executes"),
        Line2D([0], [0], color=COLORS["gap"], lw=4.2,
               solid_capstyle="butt", label="gap"),
    ]
    ax.legend(
        handles=handles,
        frameon=False,
        ncol=1,
        loc="lower right",
        bbox_to_anchor=(1.04, 0.02),
        handlelength=1.15,
        columnspacing=0.70,
        borderaxespad=0.2,
        fontsize=6.5,
    )



def panel_rank_agreement(ax, head_to_head):
    corr = head_to_head["correlations_with_GT"]
    tau_l2b = corr["L2b (code executes)"]["kendall_tau"]
    l4_vals = [
        corr["L4 section-aware (S2)"]["kendall_tau"],
        corr["L4 latter-half (S1)"]["kendall_tau"],
    ]
    l4_lo, l4_hi = min(l4_vals), max(l4_vals)

    ax.axvline(0, color=COLORS["axis"], linewidth=0.70, zorder=1)
    ax.hlines(1, 0, tau_l2b, color=COLORS["exec"], linewidth=3.5,
              zorder=2, capstyle="round")
    ax.scatter([tau_l2b], [1], color=COLORS["exec"], s=28,
               edgecolor="white", linewidth=0.55, zorder=3)
    ax.text(tau_l2b + 0.045, 1, f"{tau_l2b:+.2f}", ha="left", va="center",
            fontsize=7.0, color=COLORS["exec"], fontweight="bold")

    ax.hlines(0, l4_lo, l4_hi, color=COLORS["text"], linewidth=2.5,
              zorder=2, capstyle="round")
    ax.scatter(l4_vals, [0, 0], color=COLORS["text"], s=26,
               edgecolor="white", linewidth=0.55, zorder=3)
    ax.text((l4_lo + l4_hi) / 2, -0.235, f"{l4_lo:+.2f} to {l4_hi:+.2f}",
            ha="center", va="center", fontsize=6.7, color=COLORS["text"])

    ax.set_yticks([1, 0])
    ax.set_yticklabels(["", ""])
    ax.set_xlim(-1.00, 1.00)
    ax.set_xticks([-1.0, -0.5, 0, 0.5, 1.0])
    clean_axis(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Kendall \u03c4 vs. L2b+ rank", fontsize=7.8)
    ax.set_ylim(-0.62, 1.48)
    ax.set_title("(b) Rank agreement with L2b+",
                 loc="left", pad=3, fontsize=8.2)
    ax.text(-0.95, 1, "L2b\nexecution", ha="left", va="center",
            fontsize=6.4, color=COLORS["ink"], linespacing=0.92)
    ax.text(-0.95, 0, "L4\ntext direction", ha="left", va="center",
            fontsize=6.4, color=COLORS["ink"], linespacing=0.92)


def panel_exp_a_text_agreement(ax, exp_a):
    label_offsets = {
        "Sonnet": (-8, 10),
        "Opus": (7, 3),
        "Kimi": (7, 8),
        "GPT-4o": (-10, -8),
        "Gemini": (7, -8),
        "o3": (7, -10),
        "GPT-5": (7, -8),
    }
    label_align = {
        "Sonnet": ("right", "bottom"),
        "Opus": ("left", "center"),
        "Kimi": ("left", "bottom"),
        "GPT-4o": ("right", "top"),
        "Gemini": ("left", "top"),
        "o3": ("left", "top"),
        "GPT-5": ("left", "top"),
    }
    models = [m for m in MODEL_ORDER if m in exp_a]
    for model in models:
        x = exp_a[model]["L3"]
        y = exp_a[model]["L4"]
        ax.scatter(
            x, y,
            s=48,
            color=MODEL_COLORS[model],
            edgecolor="white",
            linewidth=0.60,
            alpha=0.95,
            zorder=3,
        )
        dx, dy = label_offsets[model]
        ha, va = label_align[model]
        ax.annotate(
            model,
            xy=(x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            ha=ha,
            va=va,
            fontsize=6.8,
            color=COLORS["ink"],
            zorder=4,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.72, pad=0.35),
        )

    ax.axvline(75, color="#DDE3EA", linewidth=0.80, alpha=0.80, zorder=0)
    ax.axhline(75, color="#DDE3EA", linewidth=0.80, alpha=0.80, zorder=0)
    ax.set_xlim(60, 91)
    ax.set_ylim(72, 88.8)
    ax.set_xticks([60, 70, 80, 90])
    ax.set_yticks([72, 76, 80, 84, 88])
    clean_axis(ax, None)
    ax.grid(True, axis="both", zorder=0)
    ax.set_xlabel("Exp A L3 method agreement (%)", fontsize=7.6)
    ax.set_ylabel("Exp A L4 direction agreement (%)", fontsize=7.6)
    ax.set_title("(c) Exp A text agreement", loc="left", pad=3, fontsize=8.2)


def make_l4_scorer_instability_appendix(multi_scorer):
    scorers = [
        "S1_latter_half_l4",
        "S2_section6_l4",
        "S3_llm_judge_l4",
        "S4_structured_l4",
    ]
    models = [m for m in MODEL_ORDER if m in multi_scorer]
    fig, ax = plt.subplots(figsize=(5.9, 2.45))
    y = np.arange(len(models))
    for yi, model in zip(y, models):
        rates = np.array([multi_scorer[model][s] * 100 for s in scorers])
        ax.hlines(yi, rates.min(), rates.max(), color=COLORS["grid"],
                  linewidth=2.7, zorder=1)
        for rate in rates:
            ax.scatter(rate, yi, s=22, color="#334155",
                       edgecolor="white", linewidth=0.35, zorder=3)
        ax.text(104, yi, f"{rates.max() - rates.min():.0f}pp",
                fontsize=7.0, color=COLORS["muted"], va="center",
                ha="left", clip_on=False)

    ax.set_yticks(y)
    ax.set_yticklabels(models)
    ax.invert_yaxis()
    ax.set_xlim(0, 110)
    ax.set_xticks([0, 25, 50, 75, 100])
    clean_axis(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("L4 pass rate across text scorers (%)")
    ax.set_title(
        "L4 scorer-operationalization diagnostic",
        loc="center",
        pad=4,
        fontsize=9.0,
        fontfamily="sans-serif",
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.subplots_adjust(left=0.16, right=0.92, top=0.86, bottom=0.22)
    return fig


def main() -> None:
    set_cv_style()
    canonical = load_json("experiments/exp_b/l2b_plus_summary_canonical.json")
    v2 = load_json("experiments/exp_b/l2b_plus_summary_canonical_judge_v2.json")
    head_to_head = load_json("experiments/exp_b/head_to_head_ranking.json")
    exp_a = load_exp_a_table()
    multi_scorer = load_json("experiments/exp_a/multi_scorer_summary.json")

    fig = plt.figure(figsize=(7.15, 2.38))
    gs = fig.add_gridspec(
        1, 3,
        width_ratios=[1.10, 1.00, 1.10],
        left=0.078,
        right=0.990,
        top=0.850,
        bottom=0.330,
        wspace=0.32,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])

    panel_execution_gap(ax_a, canonical, v2)
    panel_rank_agreement(ax_b, head_to_head)
    panel_exp_a_text_agreement(ax_c, exp_a)

    output_dirs = [ROOT / "paper/figures", ROOT / "paper/latex/figures"]
    for out_dir in output_dirs:
        out_dir.mkdir(parents=True, exist_ok=True)
        for stem in ("figure2_headline_v2", "fig2_l2b_plus_cascade"):
            for ext in ("pdf", "png"):
                path = out_dir / f"{stem}.{ext}"
                fig.savefig(path)
                print(f"Wrote {path}")
    plt.close(fig)

    appendix_fig = make_l4_scorer_instability_appendix(multi_scorer)
    for out_dir in output_dirs:
        for ext in ("pdf", "png"):
            path = out_dir / f"fig_l4_scorer_instability.{ext}"
            appendix_fig.savefig(path)
            print(f"Wrote {path}")
    plt.close(appendix_fig)


if __name__ == "__main__":
    main()
