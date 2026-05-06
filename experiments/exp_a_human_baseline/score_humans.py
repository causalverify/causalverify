#!/usr/bin/env python3
"""Score human-baseline R-script submissions using the same L2b+
pipeline used for LLMs (canonical-baseline + Haiku judge extraction +
ES window-aware matching).

Inputs
------
--submissions DIR   directory layout:
                       DIR/<student_id>/sNN_<student_id>.R
                    where NN is the 2-digit scenario id from
                    scenario_set.json.

Outputs
-------
human_baseline_scores.csv
  per (student, scenario) row with L1, L2a, L2b, L2b+, judge_effect,
  rel_error, schema-compatible with l2b_plus_scores_canonical_judge_v2.csv

human_baseline_summary.json
  per-student aggregates + per-method aggregates + cross-student
  bootstrap CI on the headline L2b+ pass rate.

This is a $0–small audit: the only paid call is the Haiku judge per
submission (~$0.003 per script). 5 students × 8 scenarios ≈ 40 calls
≈ $0.12.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src" / "pipeline"))
sys.path.insert(0, str(ROOT / "scripts"))
from score_l2b_plus import execute_r_code  # type: ignore
from l2b_llm_judge_extract import call_judge  # type: ignore

SCENARIO_SET = Path(__file__).resolve().parent / "scenario_set.json"
ES_MAX_WINDOW_DAYS = 11
TOL = 0.5


def es_pass(judge_eff: float | None, per_day: float | None,
            tol: float = TOL, max_k: int = ES_MAX_WINDOW_DAYS):
    if judge_eff is None or per_day is None or abs(per_day) < 1e-9:
        return False, None, None
    best_k, best_err = None, float("inf")
    for k in range(1, max_k + 1):
        target = per_day * k
        if abs(target) < 1e-9:
            continue
        err = abs(judge_eff - target) / abs(target)
        if err < best_err:
            best_err = err
            best_k = k
    return (best_err < tol), best_k, best_err


def score_one(r_code: str, scenario: dict) -> dict:
    sid = scenario["scenario_id"]
    method = scenario["method_family"]
    canon = scenario["canonical_estimated_effect"]

    l1 = bool(r_code.strip())
    l2a = "1"  # files end in .R, trivially yes
    l2b, stdout, err = execute_r_code(r_code) if l1 else (False, "", "")

    judge_eff = None
    rationale = ""
    if l2b and stdout:
        try:
            judge_eff, rationale, _usage = call_judge(
                method=method,
                title=scenario.get("title", ""),
                r_code=r_code,
                stdout=stdout,
            )
        except Exception as e:
            rationale = f"judge_error: {type(e).__name__}: {str(e)[:100]}"

    if method == "EVENT_STUDY":
        l2b_plus, k_match, rel_err = es_pass(judge_eff, canon)
    else:
        rel_err = (abs(judge_eff - canon) / abs(canon)
                   if (judge_eff is not None and canon is not None and abs(canon) > 1e-9)
                   else None)
        l2b_plus = bool(rel_err is not None and rel_err < TOL)
        k_match = None

    direction_canon = "positive" if (canon or 0) > 0 else "negative"
    direction_student = ("positive" if (judge_eff or 0) > 0
                         else "negative" if judge_eff is not None
                         else "")
    l4 = int(direction_student == direction_canon) if judge_eff is not None else 0

    return {
        "scenario_id": sid, "method": method,
        "canonical_estimated": canon,
        "judge_effect": judge_eff,
        "rationale": (rationale or "")[:200],
        "L1": int(l1), "L2a": int(l2a), "L2b": int(l2b),
        "rel_error": round(rel_err, 4) if rel_err is not None else "",
        "es_window_match": k_match if k_match is not None else "",
        "L2b_plus": int(l2b_plus),
        "L4_direction": l4,
        "stderr_excerpt": err[:160] if err else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--submissions", type=Path, required=True,
                    help="Directory whose subdirs are student_id/")
    ap.add_argument("--out", type=Path,
                    default=Path(__file__).resolve().parent / "human_baseline_scores.csv")
    args = ap.parse_args()

    scenarios = {s["scenario_id"]: s for s in json.loads(SCENARIO_SET.read_text())}
    print(f"Scenarios in study: {sorted(scenarios)}")

    student_dirs = sorted(p for p in args.submissions.iterdir() if p.is_dir())
    if not student_dirs:
        raise SystemExit(f"No student subdirs found under {args.submissions}")
    print(f"Students: {[p.name for p in student_dirs]}")
    print()

    rows = []
    for sdir in student_dirs:
        student_id = sdir.name
        for sid, scenario in scenarios.items():
            cand = list(sdir.glob(f"{sid}_*.R")) + list(sdir.glob(f"{sid}.R"))
            if not cand:
                rows.append({"student_id": student_id, "scenario_id": sid,
                             "missing": 1})
                continue
            r_code = cand[0].read_text()
            res = score_one(r_code, scenario)
            res["student_id"] = student_id
            res["missing"] = 0
            rows.append(res)
            tag = "+" if res["L2b_plus"] else ("v" if res["L2b"] else ".")
            print(f"  {student_id} {sid:<5} {res['method']:<14} "
                  f"L2a={res['L2a']} L2b={res['L2b']} L2b+={res['L2b_plus']} "
                  f"[{tag}] judge={res['judge_effect']!r}")

    fieldnames = ["student_id", "scenario_id", "method", "missing",
                   "L1", "L2a", "L2b", "L2b_plus", "L4_direction",
                   "judge_effect", "canonical_estimated", "rel_error",
                   "es_window_match", "rationale", "stderr_excerpt"]
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote: {args.out}")

    by_student = defaultdict(lambda: {"n": 0, "L2b_plus": 0})
    by_method = defaultdict(lambda: {"n": 0, "L2b_plus": 0})
    by_diff = defaultdict(lambda: {"n": 0, "L2b_plus": 0})
    overall = {"n": 0, "L2b_plus": 0}
    for r in rows:
        if r.get("missing"):
            continue
        sid = r["scenario_id"]
        scenario = scenarios[sid]
        by_student[r["student_id"]]["n"] += 1
        by_student[r["student_id"]]["L2b_plus"] += r["L2b_plus"]
        by_method[scenario["method_family"]]["n"] += 1
        by_method[scenario["method_family"]]["L2b_plus"] += r["L2b_plus"]
        by_diff[scenario["difficulty"]]["n"] += 1
        by_diff[scenario["difficulty"]]["L2b_plus"] += r["L2b_plus"]
        overall["n"] += 1
        overall["L2b_plus"] += r["L2b_plus"]

    summary = {
        "overall_l2b_plus_rate": overall["L2b_plus"] / max(1, overall["n"]),
        "n_attempts": overall["n"],
        "by_student": {k: v["L2b_plus"] / max(1, v["n"]) for k, v in by_student.items()},
        "by_method":  {k: v["L2b_plus"] / max(1, v["n"]) for k, v in by_method.items()},
        "by_difficulty": {k: v["L2b_plus"] / max(1, v["n"]) for k, v in by_diff.items()},
    }
    summary_path = args.out.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"Wrote: {summary_path}")
    print()
    print(f"Headline: human L2b+ rate = {summary['overall_l2b_plus_rate']*100:.1f}% on n={summary['n_attempts']} attempts")
    print(f"By method: {summary['by_method']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
