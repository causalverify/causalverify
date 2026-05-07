"""Figure 9 — L4 scorer-operationalization diagnostic.

Per-model L4 (direction agreement) pass rate under four frozen text scorers
S1/S2/S3/S4. Each model is a horizontal range from min(S1..S4) to max(S1..S4),
with a colored marker for each scorer. Wide ranges = scorer-fragile model.

Reads:  experiments/exp_a/multi_scorer_l4.csv (per-paper, per-model match flags)
Writes: paper/figures/fig_l4_scorer_instability.{pdf,png}
        paper/latex/figures/fig_l4_scorer_instability.{pdf,png}

Figure 9 is an appendix diagnostic. The frozen scorer sweep was run on
the six primary models (no GPT-5), so this figure shows six rows.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from palette import (  # noqa: E402
    MODEL_COLORS,
    MODEL_MARKERS,
    apply_paper_rc,
)

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "experiments/exp_a/multi_scorer_l4.csv"
OUT_DIRS = [
    ROOT / "paper/figures",
    ROOT / "paper/latex/figures",
]

# Y-axis order (top to bottom). GPT-5 is intentionally absent; the L4
# scorer-fragility sweep was run on the six primary models only.
MODEL_ORDER = ["Opus", "GPT-4o", "Sonnet", "o3", "Gemini", "Kimi"]

SCORERS = [
    ("S1", "S1_latter_half_match"),
    ("S2", "S2_section6_match"),
    ("S3", "S3_llm_judge_match"),
    ("S4", "S4_structured_match"),
]

GAP_COLOR = "#94A3B8"


def compute_rates() -> dict[str, dict[str, float]]:
    df = pd.read_csv(SRC)
    df = df[df.gt_direction.notna() & (df.gt_direction != "")]
    rates: dict[str, dict[str, float]] = {}
    for model in MODEL_ORDER:
        sub = df[df.model == model]
        rates[model] = {
            label: float(sub[col].mean() * 100) for label, col in SCORERS
        }
    return rates


def main() -> None:
    apply_paper_rc()

    rates = compute_rates()

    fig, ax = plt.subplots(figsize=(7.5, 3.4))

    y_positions = list(range(len(MODEL_ORDER)))[::-1]  # top row = first model

    for y, model in zip(y_positions, MODEL_ORDER):
        scorer_rates = rates[model]
        values = list(scorer_rates.values())
        v_min, v_max = min(values), max(values)
        spread = v_max - v_min

        # Range line
        ax.plot(
            [v_min, v_max],
            [y, y],
            color=GAP_COLOR,
            linewidth=2.4,
            solid_capstyle="round",
            zorder=2,
        )

        # Per-scorer markers — colored using the model's canonical (color, shape)
        color = MODEL_COLORS[model]
        marker = MODEL_MARKERS[model]
        for value in values:
            ax.scatter(
                value,
                y,
                s=80,
                color=color,
                marker=marker,
                edgecolor="black",
                linewidth=0.7,
                zorder=3,
            )

        # Spread label on the right
        ax.text(
            107,
            y,
            f"{spread:.0f}pp",
            ha="left",
            va="center",
            fontsize=9,
            color=color,
            fontweight="bold",
        )

    # Title
    ax.set_title("L4 scorer-operationalization diagnostic", pad=8)

    # Axis cosmetics
    ax.set_yticks(y_positions)
    ax.set_yticklabels(MODEL_ORDER)
    ax.set_xlim(0, 105)
    ax.set_ylim(-0.6, len(MODEL_ORDER) - 0.4)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("L4 pass rate across text scorers (%)", fontsize=10, labelpad=5)
    ax.tick_params(axis="x", length=3, color="black")
    ax.tick_params(axis="y", length=0)

    fig.tight_layout()

    for d in OUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        for ext in ("pdf", "png"):
            out = d / f"fig_l4_scorer_instability.{ext}"
            plt.savefig(out, format=ext, bbox_inches="tight", dpi=300)
            print(f"  ✓ {out}")
    plt.close()


if __name__ == "__main__":
    main()
