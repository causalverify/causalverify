#!/usr/bin/env python3
"""Scenario-clustered bootstrap CI for the L2b vs L2b+ ranking correlation.

Resamples the 100 Exp B scenarios with replacement (cluster bootstrap), recomputes
each model's L2b and L2b+ pass rate on the bootstrapped scenario set, ranks the
seven primary models on each metric, and computes Kendall tau and Spearman rho
between the two rankings. Reports point estimate, 95 percent percentile CI, and
the proportion of bootstrap tau values that exceed +0.10 (the L4 vs L2b+ tau
upper bound reported in the paper).

Output: paper/derived_analyses/bootstrap_tau_ci.json

The script does not modify any frozen CSV.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv"
OUT = ROOT / "paper/derived_analyses/bootstrap_tau_ci.json"

PRIMARY = ["Opus", "Sonnet", "GPT-4o", "o3", "Kimi", "Gemini", "GPT-5"]
B = 1000
SEED = 20260507
L4_TAU_UPPER = 0.10


def main() -> None:
    df = pd.read_csv(SRC)
    df = df[df.model.isin(PRIMARY)].copy()
    scenarios = sorted(df.scenario_id.unique())
    n_scen = len(scenarios)

    pivot_l2b = df.pivot_table(index="scenario_id", columns="model", values="L2b", aggfunc="first")
    pivot_l2bplus = df.pivot_table(
        index="scenario_id", columns="model", values="L2b_plus_v2", aggfunc="first"
    )
    pivot_l2b = pivot_l2b.reindex(index=scenarios, columns=PRIMARY)
    pivot_l2bplus = pivot_l2bplus.reindex(index=scenarios, columns=PRIMARY)

    point_l2b = pivot_l2b.mean()
    point_l2bplus = pivot_l2bplus.mean()
    tau_point, _ = kendalltau(point_l2b.values, point_l2bplus.values)
    rho_point, _ = spearmanr(point_l2b.values, point_l2bplus.values)

    rng = np.random.default_rng(SEED)
    taus = np.empty(B)
    rhos = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n_scen, size=n_scen)
        sub_l2b = pivot_l2b.iloc[idx].mean()
        sub_l2bplus = pivot_l2bplus.iloc[idx].mean()
        t, _ = kendalltau(sub_l2b.values, sub_l2bplus.values)
        r, _ = spearmanr(sub_l2b.values, sub_l2bplus.values)
        taus[b] = t
        rhos[b] = r

    tau_lo, tau_hi = float(np.quantile(taus, 0.025)), float(np.quantile(taus, 0.975))
    rho_lo, rho_hi = float(np.quantile(rhos, 0.025)), float(np.quantile(rhos, 0.975))
    prob_exceeds = float(np.mean(taus > L4_TAU_UPPER))

    out = {
        "tau_point": float(tau_point),
        "tau_ci_low": tau_lo,
        "tau_ci_high": tau_hi,
        "spearman_point": float(rho_point),
        "spearman_ci_low": rho_lo,
        "spearman_ci_high": rho_hi,
        "prob_exceeds_L4_upper": prob_exceeds,
        "L4_upper_threshold": L4_TAU_UPPER,
        "n_bootstrap": B,
        "n_scenarios": n_scen,
        "seed": SEED,
        "primary_models": PRIMARY,
        "source_csv": str(SRC.relative_to(ROOT)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))

    if abs(out["tau_point"] - 0.81) > 0.005:
        raise SystemExit(
            f"FAIL: tau point estimate {out['tau_point']:.4f} drifts from headline 0.81 "
            f"by more than 0.005. Investigate before editing the paper."
        )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
