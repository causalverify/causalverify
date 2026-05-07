# Exp B Failure Taxonomy Audit

This is a diagnostic audit, not a replacement for L2b+ scoring. It uses
existing frozen score rows, model outputs, and the existing judge cache to
classify Exp B non-L2b+ cells for the primary seven models.

The categories are conservative and rule-based. Ambiguous cases are not
forced into precise categories. No new model calls were made, no model
outputs were modified, and frozen headline L2b+ scores are unchanged.

## Scope

- Primary cells audited: 700
- Non-L2b+ failure cells classified: 340
- Executed but non-L2b+ cells: 66
- Ambiguous / uncategorized cells: 0

## Top Failure Categories

| Category                       | Count |
| ------------------------------ | ----- |
| execution_failure              | 230   |
| no_code_or_unparseable         | 44    |
| executed_wrong_coefficient     | 26    |
| coefficient_not_reported       | 15    |
| event_window_or_scale_mismatch | 11    |
| iv_first_stage_or_wrong_stage  | 5     |
| rdd_cutoff_or_sign_convention  | 3     |
| wrong_target_variable          | 2     |

## Broad Failure Groups

| Group                                          | Count |
| ---------------------------------------------- | ----- |
| Code present but execution failed              | 230   |
| No code or unparseable code block              | 44    |
| Executed and effect extracted, but L2b+ failed | 40    |
| Executed but no extractable treatment effect   | 26    |

## Files

- `failure_taxonomy_primary7.csv`
- `failure_taxonomy_by_method.csv`
- `failure_taxonomy_examples.md`
- `summary.json`
