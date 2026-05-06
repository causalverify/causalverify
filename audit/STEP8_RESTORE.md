# Step 8 restore note

Date: 2026-04-29

Purpose: reverse an over-aggressive cleanup from Step 8.

## Restored

The following Gemini calibration cache files were restored from the recorded
JSON content observed during Step 8 verification:

- `experiments/exp_b/calibration_cache/s07_gemini-2.5-flash.json`
- `experiments/exp_b/calibration_cache/s13_gemini-2.5-flash.json`
- `experiments/exp_b/calibration_cache/s23_gemini-2.5-flash.json`
- `experiments/exp_b/calibration_cache/s26_gemini-2.5-flash.json`
- `experiments/exp_b/calibration_cache/s27_gemini-2.5-flash.json`

After restoration, Gemini calibration cache coverage matches the frozen
calibration CSV:

- `calibration_scores.csv`: Gemini n=48
- `calibration_cache/*gemini-2.5-flash.json`: Gemini n=48
- CSV-not-cache difference: empty

The pre-GPT-5 calibration CSV backup was also reconstructed from the frozen
`calibration_scores.csv` by removing GPT-5 rows and the five post-backup Gemini
rows listed above:

- `experiments/exp_b/calibration_scores.csv.bak_pre_gpt5`
- Reconstructed rows: 542
- Per-model counts: Opus=100, Sonnet=99, GPT-4o=100, o3=100, Kimi=100,
  Gemini=43

## Not exactly restorable

`audit/gt_reextract_multi.json.preStage8.2` was an untracked local backup and
was not recoverable from Git after deletion. The official tracked legacy files
remain:

- `audit/gt_reextract_multi_v2_legacy.json`
- `audit/gt_aggregate_decisions_v2_legacy.json`

Those tracked files should be used for v2-era GT provenance.
