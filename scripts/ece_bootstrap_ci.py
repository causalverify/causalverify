#!/usr/bin/env python3
"""Per-model ECE bootstrap CI for numerical confidence.

Joins calibration_scores.csv to the frozen v2 correctness labels (same join
used by recompute_calibration_summary_v2.py), then bootstraps each model's
calibration records (resampled with replacement) and recomputes ECE on
10 equal-width bins per resample. Reports point estimate plus 2.5 / 97.5
percentile CI.

Output: paper/derived_analyses/ece_bootstrap_ci.csv
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CAL_CSV = ROOT / "experiments/exp_b/calibration_scores.csv"
V2_CSV = ROOT / "experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv"
OUT = ROOT / "paper/derived_analyses/ece_bootstrap_ci.csv"

PRIMARY = ["Opus", "Sonnet", "GPT-4o", "o3", "Kimi", "Gemini", "GPT-5"]
N_BINS = 10
B = 1000
SEED = 20260507

POINT_ECE = {  # from calibration_summary_v2.json (sanity-check anchors)
    "Opus": 0.3508,
    "Sonnet": 0.1530,
    "GPT-4o": 0.0995,
    "o3": 0.1389,
    "Kimi": 0.5260,
    "Gemini": 0.1800,
    "GPT-5": 0.2800,
}


def compute_ece(conf: np.ndarray, correct: np.ndarray, n_bins: int = N_BINS) -> float:
    n = len(conf)
    if n == 0:
        return 0.0
    idx = np.minimum((conf * n_bins).astype(int), n_bins - 1)
    ece = 0.0
    for b in range(n_bins):
        mask = idx == b
        nb = int(mask.sum())
        if nb == 0:
            continue
        b_conf = conf[mask].mean()
        b_acc = correct[mask].mean()
        ece += (nb / n) * abs(b_conf - b_acc)
    return float(ece)


def main() -> None:
    v2 = pd.read_csv(V2_CSV)[["scenario_id", "model_slug", "L2b_plus_v2"]]
    cal = pd.read_csv(CAL_CSV)
    df = cal.merge(v2, on=["scenario_id", "model_slug"], how="inner")

    rng = np.random.default_rng(SEED)
    rows = []
    for model in PRIMARY:
        sub = df[df.model_short == model]
        conf = sub.numerical_confidence.to_numpy(dtype=float)
        correct = sub.L2b_plus_v2.to_numpy(dtype=float)
        n = len(conf)
        if n == 0:
            rows.append({"model": model, "n": 0, "ece_point": float("nan"),
                         "ece_ci_low": float("nan"), "ece_ci_high": float("nan")})
            continue

        ece_point = compute_ece(conf, correct)
        anchor = POINT_ECE.get(model)
        if anchor is not None and abs(ece_point - anchor) > 0.005:
            raise SystemExit(
                f"FAIL: ECE drift for {model}: bootstrap point {ece_point:.4f} vs "
                f"summary anchor {anchor:.4f} (>0.005)."
            )

        boots = np.empty(B)
        for b in range(B):
            idx = rng.integers(0, n, size=n)
            boots[b] = compute_ece(conf[idx], correct[idx])
        lo, hi = float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))
        rows.append({
            "model": model,
            "n": n,
            "ece_point": round(ece_point, 4),
            "ece_ci_low": round(lo, 4),
            "ece_ci_high": round(hi, 4),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["model", "n", "ece_point", "ece_ci_low", "ece_ci_high"])
        w.writeheader()
        w.writerows(rows)

    for r in rows:
        print(f"{r['model']:<7} n={r['n']:>3}  "
              f"ECE={r['ece_point']:.3f}  CI=[{r['ece_ci_low']:.3f}, {r['ece_ci_high']:.3f}]")
    print(f"\nWrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
