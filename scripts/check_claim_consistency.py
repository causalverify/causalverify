#!/usr/bin/env python3
"""Check frozen CausalVerify submission documentation/artifact consistency.

The script catches stale CAUSAL-BENCH-era language and verifies that reviewer
navigation docs point to existing frozen artifacts. It does not rerun
experiments and does not require network access or API keys.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL_TITLE = "CausalVerify: An Execution-Grounded Benchmark for LLM Causal Inference Workflows"


DOCS = [
    "README.md",
    "DATASHEET.md",
    "RELEASE_NAVIGATION.md",
    "audit/SUBMISSION_BUILD_SUMMARY.md",
]
RELEASE_NAVIGATION_ARTIFACTS = [
    "paper/latex/causalverify_neurips2026.pdf",
    "paper/latex/causalverify_neurips2026.tex",
    "audit/SUBMISSION_BUILD_SUMMARY.md",
    "experiments/exp_a/auto_scores.csv",
    "paper/tables/exp_a_l3_l4_by_model.csv",
    "experiments/exp_b/l2b_plus_scores_canonical_judge_v2.csv",
    "experiments/exp_b/l2b_plus_summary_canonical_judge_v2.json",
    "experiments/exp_b/head_to_head_ranking.json",
    "experiments/exp_b/calibration_summary_v2.json",
    "audit/human_gold/human_vs_llm_consensus.md",
    "paper/figures/fig2_l2b_plus_cascade.pdf",
    "paper/figures/fig3_method_dotplot.pdf",
    "paper/figures/fig4_cascade.pdf",
    "paper/figures/fig_error_cdf.pdf",
    "paper/figures/calibration_reliability.pdf",
    "audit/exp_b_robustness/README.md",
    "paper/tables/exp_b_l2b_conditional_primary7.csv",
    "paper/tables/exp_b_scorer_evolution_primary7.csv",
    "paper/tables/exp_b_l2bplus_by_model_method_primary7.csv",
    "paper/tables/exp_b_tolerance_sweep_primary7.csv",
    "audit/l2b_judge_human_validation/README.md",
    "audit/l2b_judge_human_validation/annotation_form.csv",
    "scripts/prepare_l2b_judge_human_validation.py",
    "scripts/summarize_l2b_judge_human_validation.py",
]
STALE_PATTERNS = [
    (r"CAUSAL-BENCH", "legacy benchmark name"),
    (r"N=45\b|\b45 papers\b", "legacy Exp A N=45"),
    (r"N=30\b|\b30 scenarios\b", "legacy Exp B N=30"),
    (r"\b270 outputs\b|\b270 \(45 papers x 6 models\)", "legacy 45x6 output count"),
    (r"\b180 outputs\b|\b180 \(30 scenarios x 6 models\)", "legacy 30x6 output count"),
    (r"n_papers\s*=\s*57", "legacy n_papers=57 example"),
    (r"official evaluation script[^.\n]*CAUSAL-BENCH", "stale 'official scorer' claim"),
]

# Active code/script paths that must not contain stale terms.
# legacy/ is exempt (audit-only).
CODE_PATHS = [
    "evaluate.py",
]
CODE_DIRS = [
    "scripts",
    "src",
]
EXEMPT_PREFIXES = (
    "legacy/",
    # The checker itself defines the regex patterns it forbids; exempt
    # it from self-scanning to avoid pattern-definition false positives.
    "scripts/check_claim_consistency.py",
    # Tier-2 helper scripts use "30 scenarios" to describe a subset size
    # they choose, not the legacy Exp B N=30. Their docstrings reference
    # CAUSAL-BENCH only when explaining what they replaced.
    "scripts/tier2_",
)


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require_path(errors: list[str], path: str) -> None:
    if not (ROOT / path).exists():
        fail(errors, f"missing artifact: {path}")


def require_text(errors: list[str], path: str, pattern: str, label: str) -> None:
    text = read_text(path)
    if not re.search(pattern, text):
        fail(errors, f"{path}: missing {label}")


def forbid_text(errors: list[str], path: str, pattern: str, label: str) -> None:
    """Flag a stale pattern unless it appears only in clearly historical
    context (e.g. ``legacy CAUSAL-BENCH-era``, ``pre-CausalVerify``).
    """
    text = read_text(path)
    # Strip lines that are explicitly historical references — those are
    # not active claims about the current benchmark.
    historical_markers = (
        "legacy", "pre-CausalVerify", "pre-final", "audit-only",
        "-era ", "-era,", "-era.", "-era)",
        "historical", "previously", "supersede", "replaced by",
        "Expand CausalVerify Exp A corpus from 137",  # legitimate dev script
    )
    active_lines = [
        ln for ln in text.splitlines()
        if not any(marker in ln for marker in historical_markers)
    ]
    active_text = "\n".join(active_lines)
    if re.search(pattern, active_text):
        fail(errors, f"{path}: stale {label}")


def main() -> int:
    errors: list[str] = []

    for doc in DOCS:
        require_path(errors, doc)
        for pattern, label in STALE_PATTERNS:
            forbid_text(errors, doc, pattern, label)

    # Active code paths must also be free of stale terms.
    code_files: list[str] = list(CODE_PATHS)
    for code_dir in CODE_DIRS:
        for p in (ROOT / code_dir).rglob("*"):
            if not p.is_file():
                continue
            if p.suffix not in (".py", ".sh", ".md", ".yaml", ".yml"):
                continue
            rel = p.relative_to(ROOT).as_posix()
            if rel.startswith(EXEMPT_PREFIXES):
                continue
            code_files.append(rel)
    for code in sorted(set(code_files)):
        if not (ROOT / code).exists():
            continue
        if any(code.startswith(p) or code == p for p in EXEMPT_PREFIXES):
            continue
        for pattern, label in STALE_PATTERNS:
            forbid_text(errors, code, pattern, label)

    # Current key numbers must be present where the reviewer-facing docs state
    # benchmark scope. README and DATASHEET are broad docs; release navigation
    # and v12 summary carry compact frozen-scope statements.
    for doc in DOCS:
        require_text(errors, doc, r"\b259\b", f"{doc} current Exp A N=259")
        require_text(errors, doc, r"\b100\b", f"{doc} current Exp B N=100")
        require_text(errors, doc, r"\b1813\b", f"{doc} current Exp A outputs=1813")
        require_text(errors, doc, r"\b700\b", f"{doc} current Exp B primary cells=700")
        require_text(errors, doc, r"\b646\b", f"{doc} current calibration records=646")

    require_text(errors, "README.md", r"LICENSE_DATA\.md", "README links LICENSE_DATA.md")
    require_text(errors, "README.md", r"DATASHEET\.md", "README links DATASHEET.md")
    require_text(
        errors,
        "README.md",
        r"paper/latex/causalverify_neurips2026\.pdf",
        "README points to final submission PDF",
    )
    require_text(
        errors,
        "RELEASE_NAVIGATION.md",
        r"paper/latex/causalverify_neurips2026\.pdf",
        "release nav points to final submission PDF",
    )
    require_text(
        errors,
        "README.md",
        r"canonical estimator on the realised dataset",
        "README canonical-estimator wording",
    )
    require_text(errors, "README.md", r"Llama-3\.3-70B", "README names Llama robustness model")
    require_text(errors, "README.md", r"robustness check", "README Llama robustness wording")
    require_text(errors, "README.md", r"exclude[s]? Llama", "README primary ranking excludes Llama")
    require_text(errors, "RELEASE_NAVIGATION.md", r"Llama-3\.3-70B", "release nav names Llama robustness model")
    require_text(errors, "RELEASE_NAVIGATION.md", r"robustness check", "release nav Llama robustness wording")
    require_text(errors, "RELEASE_NAVIGATION.md", r"head_to_head_ranking\.json", "release nav primary ranking artifact")
    require_text(
        errors,
        "RELEASE_NAVIGATION.md",
        r"audit/exp_b_robustness/README\.md",
        "release nav links Exp B robustness audit",
    )
    require_text(
        errors,
        "RELEASE_NAVIGATION.md",
        r"audit/l2b_judge_human_validation/README\.md",
        "release nav links L2b judge human-validation scaffold",
    )
    require_text(errors, "DATASHEET.md", r"4-LLM consensus labels", "DATASHEET 4-LLM labels")
    require_text(errors, "DATASHEET.md", r"30-paper human ambiguity audit", "DATASHEET human ambiguity audit")
    require_text(
        errors,
        "DATASHEET.md",
        r"execution-grounded correctness",
        "DATASHEET L2b+ correctness endpoint wording",
    )

    for artifact in RELEASE_NAVIGATION_ARTIFACTS:
        require_path(errors, artifact)

    paper_tex = read_text("paper/latex/causalverify_neurips2026.tex")
    tex_single_line = re.sub(r"\s+", " ", paper_tex.replace("\\\\", " "))
    if FINAL_TITLE not in tex_single_line:
        fail(errors, "causalverify_neurips2026.tex must contain the final paper title")
    if r"\usepackage[eandd]{neurips_2026}" not in paper_tex:
        fail(errors, "causalverify_neurips2026.tex must use official anonymous E&D style")
    if "nonanonymous" in paper_tex:
        fail(errors, "causalverify_neurips2026.tex must not contain nonanonymous")

    require_text(errors, "README.md", re.escape(FINAL_TITLE), "README final paper title")
    require_text(errors, "audit/SUBMISSION_BUILD_SUMMARY.md", re.escape(FINAL_TITLE), "submission summary final paper title")

    for doc in ["README.md", "RELEASE_NAVIGATION.md", "audit/SUBMISSION_BUILD_SUMMARY.md"]:
        text = read_text(doc)
        for stale in ("neurips_v10", "neurips_v11", "neurips_v12"):
            for m in re.finditer(rf"\b{stale}\b", text):
                start = text.rfind("\n", 0, m.start()) + 1
                end = text.find("\n", m.end())
                line = text[start:end if end != -1 else len(text)]
                if re.search(r"removed|deleted|legacy|earlier|prior", line, re.IGNORECASE):
                    continue
                fail(errors, f"{doc}: stale legacy version reference '{stale}' (file is deleted)")
                break

    ranking = json.loads(read_text("experiments/exp_b/head_to_head_ranking.json"))
    if ranking.get("n_models") != 7:
        fail(errors, "head_to_head_ranking.json: n_models must remain 7")
    ranking_blob = json.dumps(ranking.get("rankings", {}))
    if "Llama" in ranking_blob:
        fail(errors, "head_to_head_ranking.json: Llama must not appear in primary rankings")

    hv_readme_path = ROOT / "audit/l2b_judge_human_validation/README.md"
    hv_summary_path = ROOT / "audit/l2b_judge_human_validation/summary.json"
    if hv_readme_path.exists():
        hv_text = hv_readme_path.read_text(encoding="utf-8")
        completed = 0
        if hv_summary_path.exists():
            try:
                hv_summary = json.loads(hv_summary_path.read_text(encoding="utf-8"))
                completed = int(hv_summary.get("n_annotated") or hv_summary.get("n_completed_annotations") or 0)
            except (json.JSONDecodeError, ValueError, TypeError):
                fail(errors, "l2b judge human-validation summary.json is not valid JSON")
        completion_claim = re.search(
            r"(?i)(human[- ]validation (?:is )?(?:complete|completed)|"
            r"completed human[- ]validation|final human[- ]validation metrics)",
            hv_text,
        )
        if completion_claim and completed <= 0:
            fail(
                errors,
                "l2b judge human-validation README claims completion but summary.json "
                "does not report nonzero completed annotations",
            )

    # ---- No-new-LLM reproduction-path enforcement ---------------------
    # Reviewer-facing docs that promise "no new LLM calls" must not
    # advertise `l2b_llm_judge_extract.py --all` without the
    # `--cache-only` flag, because the script otherwise calls Anthropic
    # on cache miss.
    nollm_docs = ["README.md", "RELEASE_NAVIGATION.md"]
    for doc in nollm_docs:
        if not (ROOT / doc).exists():
            continue
        text = read_text(doc)
        # Find every command that invokes l2b_llm_judge_extract.py with --all.
        for m in re.finditer(
            r"l2b_llm_judge_extract\.py[^\n]*--all[^\n]*", text
        ):
            line = m.group(0)
            if "--cache-only" not in line:
                fail(
                    errors,
                    f"{doc}: '{line.strip()}' must include --cache-only "
                    f"in the no-new-LLM reproduction path "
                    f"(otherwise the script may call Anthropic on cache miss)",
                )

    # ---- Human-coder baseline: completeness + blinding guard ----------
    hcb_dir = ROOT / "audit/human_coder_baseline"
    if hcb_dir.exists():
        hcb_summary_path = hcb_dir / "summary.json"
        hcb_completed = 0
        if hcb_summary_path.exists():
            try:
                hcb_summary = json.loads(hcb_summary_path.read_text(encoding="utf-8"))
                hcb_completed = int(hcb_summary.get("n_completed_submissions") or 0)
            except (json.JSONDecodeError, ValueError, TypeError):
                fail(errors,
                     "human_coder_baseline summary.json is not valid JSON")
        hcb_readme = hcb_dir / "README.md"
        if hcb_readme.exists() and hcb_completed <= 0:
            text = hcb_readme.read_text(encoding="utf-8")
            historical = ("incomplete", "until", "until at least one",
                          "do not cite", "not been")
            for ln in text.splitlines():
                low = ln.lower()
                if "human coder baseline" in low and (
                    "complete" in low or "completed" in low
                ):
                    if not any(h in low for h in historical):
                        fail(errors,
                             f"human_coder_baseline/README.md claims completion "
                             f"('{ln.strip()[:80]}') but summary.json reports "
                             f"n_completed_submissions={hcb_completed}")
                        break

        # Blinding: per-scenario task files (s*_task.md) must not leak
        # the canonical estimator value, the L2b+ pass label, or the DGP
        # truth parameter. INSTRUCTIONS.md and manifest.json are
        # documentation; they legitimately discuss what is NOT shared
        # and are scanned separately for actual numeric leaks.
        packet_dir = hcb_dir / "task_packet"
        if packet_dir.exists():
            numeric_leak = re.compile(
                r"canonical[_ ]estimate\s*[:=]\s*-?\d|"
                r"canonical[_ ]estimator[^\n.]{0,40}[:=]\s*-?\d|"
                r"L2b\+?\s*(?:label|pass)\s*[:=]\s*[01]|"
                r"dgp_truth\.effect\s*[:=]\s*-?\d|"
                r"true effect\s*[:=]\s*-?\d",
                re.IGNORECASE,
            )
            for p in sorted(packet_dir.glob("s*_task.md")):
                content = p.read_text(encoding="utf-8")
                if numeric_leak.search(content):
                    fail(errors,
                         f"task_packet leak: {p.relative_to(ROOT)} contains "
                         f"a canonical-estimate / L2b+ label / DGP-truth value")
            for doc in (packet_dir / "INSTRUCTIONS.md",
                        packet_dir / "manifest.json"):
                if not doc.exists():
                    continue
                content = doc.read_text(encoding="utf-8")
                if numeric_leak.search(content):
                    fail(errors,
                         f"task_packet leak: {doc.relative_to(ROOT)} prints "
                         f"a canonical-estimate / L2b+ / DGP-truth value")

    # ---- Page-budget + PDF-SHA enforcement ----------------------------
    # The submission build summary records the official NeurIPS 2026 E&D
    # page layout. The main body must be <=9 pages; references must start
    # at page <=10. The recorded SHA256 must match the actual PDF byte-
    # for-byte.
    summary_path = ROOT / "audit/SUBMISSION_BUILD_SUMMARY.md"
    pdf_path = ROOT / "paper/latex/causalverify_neurips2026.pdf"
    if summary_path.exists() and pdf_path.exists():
        s = summary_path.read_text(encoding="utf-8")
        m_main = re.search(
            r"Main content pages before References:\s*(\d+)", s)
        m_refs = re.search(r"References start:\s*page\s*(\d+)", s)
        m_sha = re.search(r"SHA256:\s*`([0-9a-fA-F]{64})`", s)
        if m_main is None:
            fail(errors, "build summary missing 'Main content pages before References'")
        elif int(m_main.group(1)) > 9:
            fail(errors,
                 f"main body pages = {m_main.group(1)} (must be <=9 per "
                 f"NeurIPS 2026 E&D limit)")
        if m_refs is None:
            fail(errors, "build summary missing 'References start: page <N>'")
        elif int(m_refs.group(1)) > 10:
            fail(errors,
                 f"references start page = {m_refs.group(1)} "
                 f"(must be <=10; otherwise main body is over the limit)")
        if m_sha is None:
            fail(errors, "build summary missing 'SHA256: `<hex>`'")
        else:
            import hashlib
            actual_sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
            if actual_sha.lower() != m_sha.group(1).lower():
                fail(errors,
                     f"build summary SHA256 ({m_sha.group(1)[:12]}...) does "
                     f"not match actual paper PDF ({actual_sha[:12]}...). "
                     f"Update audit/SUBMISSION_BUILD_SUMMARY.md.")

    if errors:
        print("Claim consistency check FAILED:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK: claim consistency checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
