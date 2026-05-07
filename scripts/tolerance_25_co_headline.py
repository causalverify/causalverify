#!/usr/bin/env python3
"""Extract the 25%-tolerance co-headline numbers for the abstract.

Reads paper/tables/exp_b_tolerance_sweep_primary7.csv, slices the 25% row,
and saves a JSON of {model: pass_rate_25} plus min and max for the abstract.

Output: paper/derived_analyses/tolerance_25_co_headline.json
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "paper/tables/exp_b_tolerance_sweep_primary7.csv"
OUT = ROOT / "paper/derived_analyses/tolerance_25_co_headline.json"

PRIMARY = ["Opus", "Sonnet", "GPT-4o", "o3", "Kimi", "Gemini", "GPT-5"]


def main() -> None:
    df = pd.read_csv(SRC)
    sub = df[df.tolerance == 0.25].set_index("model")
    rates = {m: float(sub.loc[m, "pass_rate"]) for m in PRIMARY}
    pct = {m: round(v * 100, 1) for m, v in rates.items()}
    out = {
        "tolerance": 0.25,
        "primary_models": PRIMARY,
        "pass_rate_25": rates,
        "pass_rate_25_pct": pct,
        "min_pct": min(pct.values()),
        "max_pct": max(pct.values()),
        "argmin_model": min(pct, key=pct.get),
        "argmax_model": max(pct, key=pct.get),
        "source_csv": str(SRC.relative_to(ROOT)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
