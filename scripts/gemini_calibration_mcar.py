#!/usr/bin/env python3
"""Test whether Gemini's calibration missingness (48 of 100 scenarios)
is correlated with the L2b+ outcome.

Compares L2b+ pass rates on calibrated vs missing scenarios for Gemini and
runs a chi-square test of independence between (calibrated indicator) and
(L2b+ indicator).

Output: paper/derived_analyses/gemini_mcar_check.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

ROOT = Path(__file__).resolve().parent.parent
CAL_CSV = ROOT / "experiments/exp_b/calibration_scores.csv"
V2_CSV = ROOT / "experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv"
OUT = ROOT / "paper/derived_analyses/gemini_mcar_check.json"

MODEL = "Gemini"


def main() -> None:
    cal = pd.read_csv(CAL_CSV)
    v2 = pd.read_csv(V2_CSV)
    cal_g = set(cal.loc[cal.model_short == MODEL, "scenario_id"])
    v2_g = v2[v2.model == MODEL][["scenario_id", "L2b_plus_v2"]].copy()

    v2_g["calibrated"] = v2_g.scenario_id.isin(cal_g).astype(int)

    n_cal = int(v2_g.calibrated.sum())
    n_miss = int((1 - v2_g.calibrated).sum())
    pass_cal = float(v2_g.loc[v2_g.calibrated == 1, "L2b_plus_v2"].mean())
    pass_miss = float(v2_g.loc[v2_g.calibrated == 0, "L2b_plus_v2"].mean()) if n_miss else float("nan")

    contingency = np.array([
        [int(((v2_g.calibrated == 1) & (v2_g.L2b_plus_v2 == 1)).sum()),
         int(((v2_g.calibrated == 1) & (v2_g.L2b_plus_v2 == 0)).sum())],
        [int(((v2_g.calibrated == 0) & (v2_g.L2b_plus_v2 == 1)).sum()),
         int(((v2_g.calibrated == 0) & (v2_g.L2b_plus_v2 == 0)).sum())],
    ])
    chi2, p, dof, _ = chi2_contingency(contingency, correction=False)

    out = {
        "model": MODEL,
        "n_calibrated": n_cal,
        "n_missing": n_miss,
        "pass_rate_calibrated": round(pass_cal, 4),
        "pass_rate_missing": round(pass_miss, 4) if not np.isnan(pass_miss) else None,
        "contingency_2x2": contingency.tolist(),
        "chi2_stat": round(float(chi2), 4),
        "chi2_pvalue": round(float(p), 4),
        "dof": int(dof),
        "verdict": "MCAR not rejected at 0.05" if p >= 0.05 else "MCAR rejected at 0.05",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
