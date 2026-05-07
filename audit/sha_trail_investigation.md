# SHA audit-trail investigation

**Date:** 2026-05-07
**Triggered by:** PRE-hardening SHA mismatch reported in the hardening run.
- Hardening prompt expected: `802467f3eba792f48cf72ef7bbdbc33bf26205ee103613d0ce37e3f053a49891`
- On-disk `audit/SUBMISSION_BUILD_SUMMARY.md`: `dd5ea5f57abac331628d6a6859dd63d102210b436caa60cda6c70ec7cf0eb0bb`

## Findings

### Was `802467f3...` ever committed?

**No.** `git log --all -S '802467f3'` returns no commits. The bib-fix POST SHA
that the prompt expected was never recorded in any committed version of
`audit/SUBMISSION_BUILD_SUMMARY.md`. It was a transient build artifact from a
session that ended without finalizing the summary update.

### When did `dd5ea5f...` appear?

`dd5ea5f` was committed in `e6f84be` (Thu 2026-05-07 02:12:49 +0200,
"Finalize NeurIPS submission audit package"). That commit replaced the prior
recorded SHA `c08c423...` with `dd5ea5f...`.

### Recent SHA chain in `SUBMISSION_BUILD_SUMMARY.md`

```
e6f84be (current HEAD, 2026-05-07): c08c423 -> dd5ea5f
848348b (2026-05-05):                no SHA change
4b997e6 (2026-05-05):                faa28dbc -> c08c423
5b51f41 (2026-05-05):                8b1a620b -> faa28dbc
5cf20b3 (2026-05-05):                013e7243 -> 8b1a620b
b9dd1f6 (2026-05-05):                1908687e -> 013e7243
6f4ff65 (2026-05-05):                41f6c150 -> 1908687e
d168687 (2026-05-05):                c57367b8 -> 41f6c150
a3f6f24 (2026-05-05):                0bc89254 -> c57367b8
4165bc5 (2026-05-05):                2e645aad -> 0bc89254
```

`802467f3` does not appear anywhere in this chain. The bib-fix run referenced
in the hardening prompt likely:

1. Compiled an intermediate PDF with that SHA after the bib was fixed, and
2. Did not run the final commit that would have updated the summary
   (e.g. user paused before the commit step), so
3. The next compile (driven by figure-styling commits 4165bc5 → e6f84be) overwrote
   the working PDF with a different SHA before the summary ever recorded `802467f3`.

## Conclusion

**Known audit-trail gap.** The bib-fix run did not finalize the
`SUBMISSION_BUILD_SUMMARY.md` update. There is no remediation path that
preserves history (we don't rewrite committed history). The trail will be
closed by the upcoming v11.2-camera-ready commit which records the new
post-hardening SHA, ending the chain of uncommitted intermediates.

## Recommended remediation

1. The current Phase 5 will record the new build SHA
   (post-CS-sentence and any compensation trims) in
   `audit/SUBMISSION_BUILD_SUMMARY.md`.
2. The commit message for v11.2-camera-ready notes the lineage
   `v11-freeze → bib-fix (transient 802467f3, never recorded)
   → hardening (transient 2b25e2f4) → v11.2-camera-ready (final SHA)`.
3. No history rewrite. No force operations.

This file (`audit/sha_trail_investigation.md`) is the durable record of
the gap.
