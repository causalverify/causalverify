"""Generate Figure 3: Exp A L3 method-family agreement.

Main-paper version only. The figure uses a strip plot of seven model-level
agreement rates, with paper-cluster bootstrap intervals for the cross-model
mean. This avoids treating the smaller method-family slices as equally precise.

Inputs are frozen result artifacts; this script makes no model/API calls and
does not modify scored data.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[2]

FONT_TITLE = 11
FONT_AXIS = 10
FONT_TICK = 9
FONT_TEXT = 9
FONT_LEGEND = 9

INK = "#1F2937"
AXIS = "black"  # Paper-wide: black axis lines on both x and y
GRID = "#E5E7EB"
CI_COLOR = "#374151"
MEAN_LABEL = "#374151"

MODELS_SLUG = [
    ("Claude-Opus", "Opus"),
    ("GPT-5", "GPT-5"),
    ("GPT-4o", "GPT-4o"),
    ("Claude-Sonnet", "Sonnet"),
    ("o3", "o3"),
    ("Gemini-2.5", "Gemini"),
    ("Kimi-128k", "Kimi"),
]
# Canonical (color, shape) palette — single source of truth in palette.py.
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from palette import MODEL_COLORS, MODEL_MARKERS, MODEL_ORDER as _ORDER
MODELS = _ORDER  # ["Opus", "GPT-5", "GPT-4o", "Sonnet", "o3", "Gemini", "Kimi"]

METHODS = ["Event Study", "DID", "IV", "RDD"]
METHOD_KEY = {
    "Event Study": "EVENT_STUDY",
    "IV": "IV",
    "DID": "DID",
    "RDD": "RDD",
}
DISPLAY_N = {
    "Event Study": 13,
    "IV": 32,
    "DID": 101,
    "RDD": 41,
}


def set_style() -> None:
    # Canonical paper-wide style (cream bg, dotted grid, Arial sans-serif).
    from palette import apply_paper_rc
    apply_paper_rc()


def load_l3_by_method() -> dict[str, np.ndarray]:
    with (ROOT / "experiments/exp_a/auto_scores.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))

    data = {method: [] for method in METHODS}
    key_to_method = {v: k for k, v in METHOD_KEY.items()}
    for row in rows:
        method = key_to_method.get(row.get("method", ""))
        if method is None:
            continue
        data[method].append([int(row.get(f"{slug}_L3a", 0)) for slug, _ in MODELS_SLUG])

    return {method: np.array(values, dtype=float) for method, values in data.items()}


def paper_cluster_mean_ci(values: np.ndarray, *, seed: int, n_boot: int = 10000) -> tuple[float, float, float]:
    """Return cross-model mean and a paper-cluster bootstrap 95% interval.

    Each bootstrap draw resamples papers within the method family, then computes
    each model's L3 rate and the cross-model mean. The seven model outputs for
    the same paper remain clustered together.
    """
    mean = float(values.mean(axis=0).mean() * 100)
    rng = np.random.default_rng(seed)
    n_papers = values.shape[0]
    boots = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n_papers, size=n_papers)
        boots[b] = values[idx].mean(axis=0).mean() * 100
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return mean, float(lo), float(hi)


def make_figure() -> plt.Figure:
    set_style()
    data = load_l3_by_method()
    y_pos = np.arange(len(METHODS))
    jitter = np.linspace(-0.14, 0.14, len(MODELS))

    fig, ax = plt.subplots(figsize=(6.70, 2.52))
    fig.subplots_adjust(left=0.17, right=0.985, top=0.92, bottom=0.36)

    for i, method in enumerate(METHODS):
        values = data[method]
        row_vals = values.mean(axis=0) * 100
        mean_val, ci_lo, ci_hi = paper_cluster_mean_ci(values, seed=20260506 + i)

        ax.errorbar(
            mean_val,
            i,
            xerr=[[mean_val - ci_lo], [ci_hi - mean_val]],
            fmt="D",
            markersize=4.8,
            markerfacecolor="white",
            markeredgecolor=CI_COLOR,
            markeredgewidth=0.85,
            ecolor=CI_COLOR,
            elinewidth=1.0,
            capsize=2.6,
            capthick=1.0,
            alpha=0.92,
            zorder=5,
        )
        for val, model, dy in zip(row_vals, MODELS, jitter):
            ax.scatter(
                val,
                i + dy,
                marker=MODEL_MARKERS[model],
                s=26,
                facecolors=MODEL_COLORS[model],
                edgecolors="black",
                linewidths=0.45,
                alpha=0.95,
                zorder=4,
            )

        ax.annotate(
            f"{mean_val:.0f}%",
            xy=(mean_val, i),
            xytext=(0, -4),
            textcoords="offset points",
            va="top",
            ha="center",
            fontweight="bold",
            color=MEAN_LABEL,
            fontsize=FONT_TEXT,
            zorder=5,
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{method}\n$n$={DISPLAY_N[method]}" for method in METHODS])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.55, len(METHODS) - 0.20)
    ax.invert_yaxis()
    ax.set_xlabel("L3 method-family agreement rate (%)", fontsize=FONT_AXIS, labelpad=5)
    ax.grid(axis="x", color=GRID, linestyle="-", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_color(AXIS)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(axis="y", length=0, colors=AXIS)
    ax.tick_params(axis="x", length=3, color=AXIS)

    mean_handle = Line2D(
        [0],
        [0],
        color=CI_COLOR,
        marker="D",
        markerfacecolor="white",
        markeredgecolor=CI_COLOR,
        linewidth=1.2,
        markersize=5.2,
        label="Mean + 95% CI",
    )
    legend_handles = [mean_handle] + [
        Line2D(
            [0],
            [0],
            marker=MODEL_MARKERS[model],
            color="white",
            markerfacecolor=MODEL_COLORS[model],
            markeredgecolor="black",
            markeredgewidth=0.45,
            markersize=5.0,
            label=model,
        )
        for model in MODELS
    ]
    leg = ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.50, -0.31),
        ncol=8,
        frameon=False,
        fontsize=FONT_LEGEND,
        columnspacing=0.86,
        handletextpad=0.25,
        borderaxespad=0.0,
        handlelength=1.0,
        handleheight=0.7,
        labelspacing=0.5,
    )
    leg._legend_box.align = "left"
    return fig


def main() -> None:
    fig = make_figure()
    output_specs = [
        (ROOT / "paper/figures", ("svg", "pdf", "png")),
        (ROOT / "paper/latex/figures", ("svg", "pdf", "png")),
    ]
    for out_dir, exts in output_specs:
        out_dir.mkdir(parents=True, exist_ok=True)
        for ext in exts:
            path = out_dir / f"fig3_method_dotplot.{ext}"
            fig.savefig(path)
            print(f"  ✓ {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
