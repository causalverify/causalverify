# Quarantined papers (excluded from active corpus)

These paper JSONs are kept in git history but excluded from all
benchmark pipelines. They are NOT counted in the corpus size of N=259.

## paper_203_rdd_hard.json (added 2026-04-27)

**Why excluded.** Corpus-level PDF mismatch. The metadata in
`paper_203_rdd_hard.json` (and the OpenAlex abstract for the same
DOI) describe a regression-discontinuity *methodology* paper that
discusses scholarships, financial aid, class size, school quality
etc. (Thistlethwaite-Campbell-style examples). The PDF actually at
`audit/pdfs/paper_203.pdf`, however, contains a PROGRESA evaluation
text (Mexican anti-poverty program) — a different paper. V2'' Phase 1
produced a faithful summary of the PDF (PROGRESA setup) and was
flagged as `diverges` by L3 fidelity in Stage 5.4 because the abstract
and the PDF disagree.

This is not a Phase 1 error: Phase 1 correctly described what was
in the source. The source is wrong.

**Decision.** Drop from corpus rather than re-fetch. paper_203 is one
of 50 in our L3 fidelity sample, and excluding it removes the only
diverges from the L3 audit; 47/49 remain faithful (96%) on the
remaining 49-paper sample.

**Cross-references.**

- L3 fidelity record: `audit/new_fidelity_v2primeprime.json`
- Stage 5.4 commit: `4b8cca6`

## paper_187_did_medium.json

**Why excluded.** Both the source PDF and the OpenAlex abstract are
OCR garbage (random alphanumeric noise such as
`'3 01 fl3VI 2i ,33110fl flth1JL3ni I Gfl!P1G2 [9cG nb [PG!L ...'`).
The PDF was already moved to `audit/pdfs/_scanned_quarantine/` early
in the project as a known scanned-image paper that pdfplumber and
pypdf could not extract. In Stage 4 (V2'' rebuild) on 2026-04-27,
Opus 4.7 returned `stop=refusal` on the OCR-garbage abstract, which
is correct behavior — there is no extractable research question or
data description from that input. After the empty-content fallback,
no usable source remains.

**Decision.** Drop from corpus. Document in DATASHEET / Limitations
as part of the "2 of 261 candidate papers excluded" note (paper_187
for OCR corruption, paper_203 for PDF/metadata mismatch). Final
active corpus: N=259.

**Cross-references.**

- V2'' rebuild events: `experiments_log/runs/2026-04-27/005__v2primeprime_full_text_rebuild/events.jsonl`
- SDK-fix commit: `91b4b36`
- Original PDF (still in repo for transparency):
  `audit/pdfs/_scanned_quarantine/paper_187.pdf`
