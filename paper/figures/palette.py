"""
Canonical CausalVerify color palette.

All figure scripts should import from this module to ensure visual
consistency across the paper. Modeled on fig1_v4 Morandi scheme.
"""

# ── Semantic / concept colors ──
PAL = {
    # Tasks
    "input":     "#E5D8C3",  # Exp A (real papers, beige)
    "input_d":   "#9E8B6E",

    # Models
    "model":     "#D1DFE9",
    "model_d":   "#5E8BA8",

    # Outputs
    "code":      "#5B8DB8",  # R code (cornflower blue)
    "code_d":    "#2D5A7C",

    # Novel layer (L2b+)
    "novel":     "#D4785A",  # coral
    "novel_bg":  "#FBE9E0",  # pale coral
    "novel_d":   "#8C3E1D",

    # Deterministic group (L1, L2a, L2b)
    "deter":     "#6BA898",  # seafoam green
    "deter_bg":  "#E8F5F0",
    "deter_d":   "#3E7864",

    # Text-fragile group (L3, L4)
    "fragile":   "#C89F72",  # warm tan
    "fragile_bg":"#F8EFE0",
    "fragile_d": "#8A5E38",

    # Utility / background
    "zone_bg":   "#F8F6F2",
    "zone_edge": "#E8E4DF",
    "ink":       "#1A1A1A",
    "muted":     "#6B6B6B",
    "shadow":    "#C8C8C8",
    "divider":   "#D8D2C8",
}

# ── Canonical per-model colors (used across all figures) ──
# Adapted from the Wong-Okabe-Ito 8-color color-blind-safe palette
# (Wong 2011, Nature Methods). Each model has BOTH a unique color AND
# a unique shape, so figures stay readable in B&W and under all common
# forms of color-vision deficiency.
MODEL_COLORS = {
    "Opus":    "#E69F00",  # orange (Anthropic flagship, warm)
    "Sonnet":  "#CC79A7",  # reddish purple (Anthropic, secondary)
    "GPT-4o":  "#56B4E9",  # sky blue (OpenAI mid-tier)
    "GPT-5":   "#0072B2",  # strong blue (OpenAI flagship)
    "o3":      "#009E73",  # bluish green / teal (OpenAI reasoning)
    "Kimi":    "#D55E00",  # vermillion (Moonshot)
    "Gemini":  "#F0E442",  # yellow (Google) — needs black edge to read on white
}

# Ordering for consistent bar/rank positions in legends and axis labels.
# Mirrors the L2b+ ranking from Finding 2 (descending pass rate).
MODEL_ORDER = ["Opus", "GPT-5", "GPT-4o", "Sonnet", "o3", "Gemini", "Kimi"]

# Canonical per-model marker shapes (shape + color = double encoding)
MODEL_MARKERS = {
    "Opus":   "o",   # circle
    "Sonnet": "^",   # triangle up
    "GPT-4o": "s",   # square
    "GPT-5":  "*",   # star
    "o3":     "D",   # diamond
    "Kimi":   "P",   # plus (filled)
    "Gemini": "X",   # x (filled)
}

# Llama-3.3-70B-Instruct (open-weights robustness only). De-emphasized
# in gray with a downward triangle so it never visually competes with
# the primary panel.
LLAMA_STYLE = {
    "color":  "#888888",
    "marker": "v",
    "label":  "Llama (robustness)",
}

# ── Standard scatter kwargs for model markers ──
# Centralized so all figures render at the same visual weight.
MARKER_KWARGS = dict(
    s=80,                       # area in points^2
    edgecolor="black",
    linewidth=0.7,
    alpha=0.95,
)


def style_for(model: str) -> dict:
    """Return matplotlib scatter kwargs for one model.

    Use as: ax.scatter(x, y, **style_for("Opus"))
    """
    if model in MODEL_COLORS:
        return dict(
            c=MODEL_COLORS[model],
            marker=MODEL_MARKERS[model],
            label=model,
            **MARKER_KWARGS,
        )
    if model == "Llama":
        return dict(
            c=LLAMA_STYLE["color"],
            marker=LLAMA_STYLE["marker"],
            label=LLAMA_STYLE["label"],
            **MARKER_KWARGS,
        )
    raise ValueError(f"Unknown model: {model!r}")


def line_style_for(model: str) -> dict:
    """Return matplotlib plot/line kwargs for one model (line + marker).

    Use as: ax.plot(x, y, **line_style_for("Opus"))
    """
    if model in MODEL_COLORS:
        return dict(
            color=MODEL_COLORS[model],
            marker=MODEL_MARKERS[model],
            markersize=8,
            markeredgecolor="black",
            markeredgewidth=0.5,
            linewidth=1.6,
            label=model,
        )
    if model == "Llama":
        return dict(
            color=LLAMA_STYLE["color"],
            marker=LLAMA_STYLE["marker"],
            markersize=8,
            markeredgecolor="black",
            markeredgewidth=0.5,
            linewidth=1.6,
            linestyle="--",
            label=LLAMA_STYLE["label"],
        )
    raise ValueError(f"Unknown model: {model!r}")

# ── Method family colors (used in sunburst, method-level heatmap) ──
METHOD_COLORS = {
    "DID":         "#DCCBB2",  # soft tan
    "ES":          "#C4B59A",  # darker tan
    "EVENT_STUDY": "#C4B59A",
    "IV":          "#A896C2",  # muted violet
    "RDD":         "#7FB59F",  # soft teal
}

# ── Domain colors (used in sunburst outer ring only) ──
DOMAIN_COLORS = {
    "finance":     "#5B8DB8",
    "labor":       "#9B82BB",
    "health":      "#6BA898",
    "education":   "#D4A85A",
    "development": "#D4785A",
    "public":      "#7D9CAD",
    "trade":       "#A8C5D5",
    "environment": "#8FB08E",
    "urban":       "#C8B8A6",
    "agriculture": "#E8C8A0",
}

# ── Layer-specific colors for grouped bar charts (L2a/L2b/L2b+) ──
LAYER_COLORS = {
    "L1":    PAL["deter_bg"],
    "L2a":   "#C8B8A6",        # pale beige (near-ceiling layer)
    "L2b":   PAL["code"],       # blue (code executes)
    "L2b+":  PAL["novel"],      # coral (DGP-verified)
    "L3":    PAL["fragile"],    # tan (strategy)
    "L4":    PAL["fragile"],    # tan (direction)
}

# ── Diverging colormap stops (heatmaps) ──
# Goes from pale coral (low) through beige (mid) to cornflower blue (high)
HEATMAP_STOPS = [
    (0.00, "#FBE9E0"),   # very pale coral
    (0.25, "#F2C0A0"),   # light coral
    (0.50, "#E8D8C0"),   # beige
    (0.75, "#B8D0DC"),   # pale blue
    (1.00, "#5B8DB8"),   # cornflower blue
]

# ── Standard matplotlib rcParams for all figures ──
# (Legacy; superseded by PAPER_RC below for paper-rendered figures.)
RC_PARAMS = {
    # Match NeurIPS body text (Times / serif) for visual consistency
    "font.family":       "serif",
    "font.serif":        ["Times", "Times New Roman", "Nimbus Roman", "DejaVu Serif"],
    "mathtext.fontset":  "stix",
    # Unified font-size stack for all paper figures.
    "font.size":         13,
    "axes.titlesize":    14,
    "axes.labelsize":    13,
    "xtick.labelsize":   12,
    "ytick.labelsize":   12,
    "legend.fontsize":   12,
    "figure.titlesize":  15,
    "axes.facecolor":    "#FAFAFA",
    "figure.facecolor":  "white",
    "axes.grid":         True,
    "axes.axisbelow":    True,
    "grid.color":        "#E8E4DF",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.5,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "pdf.fonttype":      42,
    "ps.fonttype":       42,
}


# ── Canonical typography + axes-style for all paper-rendered figures ──
# Single source of truth. Every figure script should call apply_paper_rc()
# before drawing, then use AXIS_LABEL_KW for set_xlabel / set_ylabel so that
# axis labels (font, size, padding) are byte-identical across figures.
#
# The visual look matches fig_rid_pilot's polished style:
#   - Cream-white axes background (#FAFAFA)
#   - Dotted gray grid behind data
#   - Light gray axis spines, no top/right
#   - Arial sans-serif typography throughout
PAPER_RC = {
    # Typography
    "font.family":       "sans-serif",
    "font.sans-serif":   ["Arial", "Helvetica", "DejaVu Sans"],
    "mathtext.fontset":  "dejavusans",
    "font.size":          9,        # body / tick text
    "axes.titlesize":    11,        # subplot title
    "axes.titleweight":  "bold",
    "axes.labelsize":    10,        # x-/y-axis label
    "xtick.labelsize":    9,
    "ytick.labelsize":    9,
    "legend.fontsize":    9,
    # Spines
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.edgecolor":    "#94A3B8",
    "axes.linewidth":    0.65,
    # Colors (cream background, ink-dark text)
    "axes.facecolor":    "#FAFAFA",
    "figure.facecolor":  "white",
    "xtick.color":       "#1F2937",
    "ytick.color":       "#1F2937",
    "axes.labelcolor":   "#1F2937",
    # Grid (dotted, behind data)
    "axes.grid":         True,
    "axes.axisbelow":    True,
    "grid.color":        "#E8E4DF",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.5,
    # Output
    "pdf.fonttype":      42,
    "ps.fonttype":       42,
    "savefig.dpi":       600,
    "savefig.bbox":      "tight",
    "savefig.pad_inches": 0.03,
}


# Canonical kwargs for ax.set_xlabel / ax.set_ylabel calls.
# Every figure should pass **AXIS_LABEL_KW so the label font, size, and
# distance-to-axis are byte-identical paper-wide.
AXIS_LABEL_KW = dict(fontsize=10, labelpad=5)


def apply_paper_rc() -> None:
    """Apply the canonical paper rcParams. Call once per figure script."""
    import matplotlib.pyplot as plt
    plt.rcParams.update(PAPER_RC)
