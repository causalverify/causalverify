#!/usr/bin/env python3
"""Check frozen CausalVerify submission documentation/artifact consistency.

The script catches stale CAUSAL-BENCH-era language and verifies that reviewer
navigation docs point to existing frozen artifacts. It does not rerun
experiments and does not require network access or API keys.
"""

from __future__ import annotations

import json
import re
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINAL_TITLE = "CausalVerify: An Execution-Grounded Benchmark for LLM Causal Inference Workflows"
HF_DATASET_RELEASE = "causalverify/causalverify-neurips2026"
HF_CODE_RELEASE = "causalverify/causalverify-code-neurips2026"
HF_SUBMISSION_TAG = "neurips2026-submission"


DOCS = [
    "README.md",
    "DATASHEET.md",
    "RELEASE_NAVIGATION.md",
    "audit/SUBMISSION_BUILD_SUMMARY.md",
]
RELEASE_NAVIGATION_ARTIFACTS = [
    "paper/latex/causalverify_neurips2026.pdf",
    "paper/latex/causalverify_neurips2026.tex",
    "audit/V11_ACCEPTANCE_GATES.md",
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
    "paper/tables/exp_b_rank_stability_primary7.csv",
    "paper/tables/exp_b_scorer_evolution_primary7.csv",
    "paper/tables/exp_b_l2bplus_by_model_method_primary7.csv",
    "paper/tables/exp_b_tolerance_sweep_primary7.csv",
    "audit/exp_b_robustness/tolerance_sweep_primary7.csv",
    "audit/exp_b_robustness/tolerance_sweep_primary7.json",
    "audit/exp_b_failure_taxonomy/README.md",
    "audit/exp_b_failure_taxonomy/failure_taxonomy_primary7.csv",
    "audit/exp_b_failure_taxonomy/failure_taxonomy_by_method.csv",
    "audit/exp_b_robustness/rank_stability_primary7.csv",
    "audit/exp_b_robustness/rank_stability_primary7.json",
    "audit/l2b_judge_human_validation/README.md",
    "audit/l2b_judge_human_validation/annotation_form.csv",
    "audit/l2b_judge_human_validation/annotation_key_private.csv",
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

# Reviewer-facing claim surfaces where ground-truth terminology is most likely
# to affect interpretation. Frozen CSV/JSON outputs and scenario metadata are
# intentionally not scanned by these wording checks.
CLAIM_LANGUAGE_PATHS = [
    "README.md",
    "DATASHEET.md",
    "RELEASE_NAVIGATION.md",
    "LICENSE_DATA.md",
    "audit/SUBMISSION_BUILD_SUMMARY.md",
    "paper/latex/causalverify_neurips2026.tex",
    "paper/latex/checklist.tex",
]
CLAIM_LANGUAGE_FIGURE_SUFFIXES = {".py", ".svg", ".tex"}
RISKY_CLAIM_LANGUAGE = [
    (r"\bExp(?:eriment)?(?:\\?~|\s)+A\s+ground[- ]truth\b",
     "Exp A ground-truth wording; use Exp A reference labels"),
    (r"\bexecutable\s+ground[- ]truth\b",
     "executable ground-truth wording; use executable reference estimates"),
    (r"\btarget\s+causal\s+estimate\b",
     "target causal estimate; use target estimate or canonical estimate"),
    (r"\bL2b\+\s+truth\b",
     "L2b+ truth wording; use L2b+ pass/fail label"),
    (r"\bhidden\s+truth\b",
     "hidden truth wording; use hidden L2b+ correctness label"),
    (r"\bhuman[- ]gold\b",
     "human-gold wording in active reviewer-facing docs"),
    (r"\bverified\s+ground[- ]truth\b",
     "verified ground-truth wording"),
    (r"(?<!not\s)(?<!not\sas\s)\bverified\s+causal\s+correctness\b",
     "verified causal-correctness wording in active reviewer-facing docs"),
    (r"\bDGP\s+true\s+effect\b",
     "DGP true effect wording as an active scoring claim"),
    (r"\bL2b\+[^.\n]{0,80}\brecovers?[^.\n]{0,80}"
     r"\b(?:true effect|DGP|ideal DGP|beta star|β\*)\b",
     "L2b+ recovery of the ideal/true DGP effect"),
    (r"\bL4\s+text\s+scoring\s+is\s+essentially\s+uncorrelated\b",
     "overbroad L4-text-scoring claim"),
    (r"\btext\s+scoring\s+is\s+useless\b",
     "overbroad text-scoring claim"),
    (r"\bself-confidence\s+does\s+not\s+identify\s+mistakes\b",
     "overbroad self-confidence heading"),
    (r"\bmodels\s+do\s+not\s+know\s+when\s+they\s+are\s+wrong\b",
     "overbroad model-self-knowledge claim"),
    (r"\bcalibration\s+is\s+impossible\b",
     "overbroad calibration impossibility claim"),
    (r"\bmodel\s+confidence\s+never\s+helps\b",
     "overbroad confidence claim"),
    (r"\blanguage-invariant\s+ranking\b",
     "overbroad language-invariant ranking claim"),
    (r"\buniversal\s+causal\s+ability\b",
     "overbroad universal causal ability claim"),
    (r"\bgeneral\s+causal\s+intelligence\b",
     "overbroad general causal intelligence claim"),
    (r"\bcomplete\s+empirical\s+researcher\b",
     "overbroad complete empirical researcher claim"),
]
EXPECTED_PRIMARY_L2B_PLUS_COUNTS = {
    "Opus": 88,
    "GPT-5": 72,
    "GPT-4o": 62,
    "Sonnet": 50,
    "o3": 46,
    "Gemini": 32,
    "Kimi": 10,
}


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


def claim_language_files() -> list[str]:
    files = list(CLAIM_LANGUAGE_PATHS)
    figures_dir = ROOT / "paper/figures"
    if figures_dir.exists():
        for p in sorted(figures_dir.rglob("*")):
            if p.is_file() and p.suffix in CLAIM_LANGUAGE_FIGURE_SUFFIXES:
                files.append(p.relative_to(ROOT).as_posix())
    return sorted(set(files))


def forbid_risky_claim_language(errors: list[str], path: str) -> None:
    if not (ROOT / path).exists():
        return
    text = read_text(path)
    for pattern, label in RISKY_CLAIM_LANGUAGE:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if (
                path == "paper/latex/causalverify_neurips2026.tex"
                and label == "target causal estimate; use target estimate or canonical estimate"
            ):
                abstract = re.search(
                    r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
                    text,
                    re.IGNORECASE | re.DOTALL,
                )
                if abstract and abstract.start() <= match.start() <= abstract.end():
                    continue
            line_no = text.count("\n", 0, match.start()) + 1
            fail(errors, f"{path}:{line_no}: {label}")

    # dgp_truth is a valid field name in scenario/Croissant metadata, but
    # reviewer-facing prose must distinguish it from the L2b+ scoring baseline.
    for match in re.finditer(r"\bdgp_truth\b", text, re.IGNORECASE):
        window = text[max(0, match.start() - 180): match.end() + 180]
        metadata_context = re.search(
            r"\b(field|metadata|schema|Croissant|scenario)\b",
            window,
            re.IGNORECASE,
        )
        distinguishes_l2b = re.search(
            r"\b(not|distinct|separate|rather than)\b[^.\n]{0,80}\bL2b\+|"
            r"\bL2b\+[^.\n]{0,80}\b(not|distinct|separate|rather than)\b|"
            r"\bcanonical estimator\b",
            window,
            re.IGNORECASE,
        )
        if not (metadata_context and distinguishes_l2b):
            line_no = text.count("\n", 0, match.start()) + 1
            fail(errors,
                 f"{path}:{line_no}: dgp_truth must appear only as a "
                 f"clearly distinguished scenario/Croissant metadata field")


def main() -> int:
    errors: list[str] = []

    for doc in DOCS:
        require_path(errors, doc)
        for pattern, label in STALE_PATTERNS:
            forbid_text(errors, doc, pattern, label)

    for doc in claim_language_files():
        forbid_risky_claim_language(errors, doc)

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
        r"audit/exp_b_failure_taxonomy/README\.md",
        "release nav links Exp B failure-taxonomy audit",
    )
    require_text(
        errors,
        "audit/exp_b_failure_taxonomy/README.md",
        r"diagnostic audit, not a replacement for L2b\+ scoring",
        "failure taxonomy is diagnostic, not replacement scoring",
    )
    require_text(
        errors,
        "audit/exp_b_failure_taxonomy/README.md",
        r"No new model calls were made",
        "failure taxonomy no-new-model-call statement",
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
    if r"\label{app:canonical_estimators}" not in paper_tex:
        fail(errors, "causalverify_neurips2026.tex must document Exp B canonical estimators")
    if not re.search(r"benchmark-defined\s+reference\s+path\s+for\s+executable\s+evaluation", paper_tex):
        fail(errors, "causalverify_neurips2026.tex must bound the canonical-estimator construct claim")
    if "not a claim that only one empirical analysis is" not in paper_tex:
        fail(errors, "causalverify_neurips2026.tex must state canonical estimator is not uniquely defensible")

    require_text(errors, "README.md", re.escape(FINAL_TITLE), "README final paper title")
    require_text(errors, "audit/SUBMISSION_BUILD_SUMMARY.md", re.escape(FINAL_TITLE), "submission summary final paper title")
    require_text(errors, "README.md", re.escape(HF_SUBMISSION_TAG), "README stable HF release tag")
    require_text(errors, "RELEASE_NAVIGATION.md", re.escape(HF_SUBMISSION_TAG), "release nav stable HF release tag")
    require_text(errors, "RELEASE_NAVIGATION.md", re.escape(HF_DATASET_RELEASE), "release nav HF dataset release")
    require_text(errors, "RELEASE_NAVIGATION.md", re.escape(HF_CODE_RELEASE), "release nav HF code release")

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

    l2b_summary = json.loads(read_text("experiments/exp_b/l2b_plus_summary_canonical_judge_v2.json"))
    if float(l2b_summary.get("tolerance", -1)) != 0.5:
        fail(errors, "l2b_plus_summary_canonical_judge_v2.json: default tolerance must remain 0.5")
    by_model = l2b_summary.get("by_model", {})
    for model, expected_count in EXPECTED_PRIMARY_L2B_PLUS_COUNTS.items():
        record = by_model.get(model)
        if not isinstance(record, dict):
            fail(errors, f"l2b_plus_summary_canonical_judge_v2.json: missing {model}")
            continue
        if int(record.get("n", -1)) != 100:
            fail(errors, f"l2b_plus_summary_canonical_judge_v2.json: {model} denominator must remain 100")
        if int(record.get("L2b_plus_v2", -1)) != expected_count:
            fail(errors, f"l2b_plus_summary_canonical_judge_v2.json: {model} L2b+ headline count changed")
        expected_rate = expected_count / 100
        if abs(float(record.get("L2b_plus_v2_rate", -1)) - expected_rate) > 1e-9:
            fail(errors, f"l2b_plus_summary_canonical_judge_v2.json: {model} L2b+ headline rate changed")

    tolerance_csv = ROOT / "audit/exp_b_robustness/tolerance_sweep_primary7.csv"
    if tolerance_csv.exists():
        with tolerance_csv.open(newline="") as f:
            tolerance_rows = list(csv.DictReader(f))
        default_rows = {r.get("model"): r for r in tolerance_rows if r.get("tolerance") == "0.50"}
        for model, expected_count in EXPECTED_PRIMARY_L2B_PLUS_COUNTS.items():
            row = default_rows.get(model)
            if row is None:
                fail(errors, f"tolerance_sweep_primary7.csv: missing 0.50 row for {model}")
                continue
            if int(row.get("denominator", -1)) != 100:
                fail(errors, f"tolerance_sweep_primary7.csv: {model} 0.50 denominator must be 100")
            if int(row.get("pass_count", -1)) != expected_count:
                fail(errors, f"tolerance_sweep_primary7.csv: {model} 0.50 count must match headline")
    tolerance_json_path = ROOT / "audit/exp_b_robustness/tolerance_sweep_primary7.json"
    if tolerance_json_path.exists():
        tolerance_payload = json.loads(tolerance_json_path.read_text(encoding="utf-8"))
        if float(tolerance_payload.get("default_headline_tolerance", -1)) != 0.5:
            fail(errors, "tolerance_sweep_primary7.json: default headline tolerance must remain 0.5")
        primary_models = tolerance_payload.get("primary_models", [])
        if "Llama" in primary_models:
            fail(errors, "tolerance_sweep_primary7.json: Llama must not appear in primary_models")

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
