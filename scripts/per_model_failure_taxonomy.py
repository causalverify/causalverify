#!/usr/bin/env python3
"""Per-model breakdown of the Exp B failure taxonomy.

Aggregates audit/exp_b_failure_taxonomy/failure_taxonomy_primary7.csv into a
per-model table that mirrors the columns of the current paper Table 7 but
splits the 340 non-L2b+ cells across the seven primary models. The categories
follow the paper's broad-group taxonomy:

  - exec_failure                  -> B_execution_failure
  - no_code                       -> A_no_code_or_unparseable
  - exec_wrong_coef               -> D_executed_wrong_coefficient (executed_wrong_coefficient)
  - coef_not_reported             -> C_executed_no_extractable_effect (coefficient_not_reported)
  - event_window_scale            -> *_event_window_or_scale_mismatch (B/C/D combined)
  - iv_stage                      -> *_iv_first_stage_or_wrong_stage
  - rdd_cutoff                    -> *_rdd_cutoff_or_sign_convention
  - other                         -> remaining sub-categories

Outputs:
  paper/derived_analyses/failure_taxonomy_by_model.csv
  paper/derived_analyses/failure_taxonomy_by_model.md
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "audit/exp_b_failure_taxonomy/failure_taxonomy_primary7.csv"
OUT_CSV = ROOT / "paper/derived_analyses/failure_taxonomy_by_model.csv"
OUT_MD = ROOT / "paper/derived_analyses/failure_taxonomy_by_model.md"

PRIMARY_ORDER = ["Opus", "Sonnet", "GPT-4o", "o3", "Kimi", "Gemini", "GPT-5"]


CATEGORIES = [
    ("exec_failure", "B_execution_failure", {"execution_failure"}),
    ("no_code", "A_no_code_or_unparseable", {"no_code_or_unparseable"}),
    ("exec_wrong_coef", "D_executed_wrong_coefficient", {"executed_wrong_coefficient"}),
    ("coef_not_reported", "C_executed_no_extractable_effect", {"coefficient_not_reported"}),
    ("event_window_scale", None, {"event_window_or_scale_mismatch"}),
    ("iv_stage", None, {"iv_first_stage_or_wrong_stage"}),
    ("rdd_cutoff", None, {"rdd_cutoff_or_sign_convention"}),
]


def main() -> None:
    raw = pd.read_csv(SRC)
    raw["count"] = raw["count"].astype(int)

    rows = []
    grand_count = 0
    grand_buckets = {key: 0 for key, _, _ in CATEGORIES}
    grand_buckets["other"] = 0

    for model in PRIMARY_ORDER:
        m = raw[raw.model == model]
        total = int(m["count"].sum())
        grand_count += total

        used_idx = set()
        buckets = {}
        for key, group_label, sub_set in CATEGORIES:
            mask = m["failure_category"].isin(sub_set)
            if group_label is not None:
                mask = mask & (m["broad_group"] == group_label)
            n = int(m.loc[mask, "count"].sum())
            buckets[key] = n
            used_idx |= set(m.index[mask].tolist())
            grand_buckets[key] += n

        other = int(m.loc[~m.index.isin(used_idx), "count"].sum())
        buckets["other"] = other
        grand_buckets["other"] += other

        row = {"model": model, "total_non_l2bplus": total}
        for key in [c[0] for c in CATEGORIES] + ["other"]:
            row[f"{key}_n"] = buckets[key]
            row[f"{key}_share"] = round(buckets[key] / total, 4) if total else 0.0
        rows.append(row)

    out = pd.DataFrame(rows)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    grand_total = sum(grand_buckets.values())
    expected_total = 340
    if grand_total != expected_total:
        raise SystemExit(
            f"FAIL: per-model totals sum to {grand_total} but Table 7 reports "
            f"{expected_total}. Check category mapping."
        )

    paper_table_buckets = {
        "exec_failure": 230,
        "no_code": 44,
        "exec_wrong_coef": 26,
        "coef_not_reported": 15,
        "event_window_scale": 11,
        "iv_stage": 5,
        "rdd_cutoff": 3,
        "other": 6,
    }
    drift = {k: (grand_buckets[k], paper_table_buckets[k]) for k in paper_table_buckets}
    bad = {k: v for k, v in drift.items() if v[0] != v[1]}
    if bad:
        raise SystemExit(
            f"FAIL: per-model rows do not reproduce paper Table 7 totals.\n"
            f"  Mismatches: {bad}"
        )

    headers = [
        "Model", "n_fail",
        "Exec fail", "No code", "Exec wrong coef", "Coef not reported",
        "Event-win/scale", "IV stage", "RDD cutoff", "Other",
    ]
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        cells = [
            r["model"], str(r["total_non_l2bplus"]),
            f'{r["exec_failure_n"]} ({100*r["exec_failure_share"]:.1f}\\%)',
            f'{r["no_code_n"]} ({100*r["no_code_share"]:.1f}\\%)',
            f'{r["exec_wrong_coef_n"]} ({100*r["exec_wrong_coef_share"]:.1f}\\%)',
            f'{r["coef_not_reported_n"]} ({100*r["coef_not_reported_share"]:.1f}\\%)',
            f'{r["event_window_scale_n"]} ({100*r["event_window_scale_share"]:.1f}\\%)',
            f'{r["iv_stage_n"]} ({100*r["iv_stage_share"]:.1f}\\%)',
            f'{r["rdd_cutoff_n"]} ({100*r["rdd_cutoff_share"]:.1f}\\%)',
            f'{r["other_n"]} ({100*r["other_share"]:.1f}\\%)',
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append(f"Grand total non-L2b+ cells: {grand_total} (matches paper Table 7).")
    OUT_MD.write_text("\n".join(lines))

    print(out.to_string(index=False))
    print(f"\nGrand total: {grand_total} (paper Table 7: {expected_total}).")
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
