# Data Audit

Use this reference whenever CSV/XLSX data are present. Run `scripts/data_profile.py` with `--input <data-or-dir> --output <tables-dir>` before modeling unless the user explicitly asks for planning only.

## Audit Outputs

The data profile should create:

- `tab_data_inventory.xlsx`: file, sheet/table, row count, column count, column list, key field candidates, time fields, numeric fields, included/excluded status.
- `tab_missing_summary.xlsx`: missing count and ratio by field.
- `tab_numeric_profile.xlsx`: count, mean, standard deviation, min, quartiles, max, and IQR outlier count.
- `tab_categorical_profile.xlsx`: unique count and top values for categorical fields.
- `tab_sheet_coverage.xlsx`: workbook sheet coverage and exclusion reasons.
- `tab_time_range_summary.xlsx`: detected time fields and min/max coverage.
- `tab_duplicate_summary.xlsx`: duplicate full-row counts by table.
- `tab_excluded_sheets.xlsx`: empty or excluded sheets that require review.
- `tab_unit_guess.xlsx`: unit hints inferred from column names.
- `tab_merge_candidates.xlsx`: same-structure tables/sheets that may be concatenated.
- `data_inventory.xlsx`: one workbook containing the main audit sheets above.
- `merged_candidates/merge_candidate_*.csv`: optional concatenated same-structure tables with `source_file` and `source_sheet`.
- `data_profile_summary.md`: judge-readable summary.
- `data_preprocessing_draft.md`: Chinese paper paragraph draft.

## Required Checks

1. List all workbook sheets before using any Excel data.
2. Confirm whether same-structure sheets should be concatenated; if yes, keep `source_file` and `source_sheet`.
3. Compare covered rows, reconstructed task counts, and time ranges against the problem statement.
4. Identify unit candidates from field names and sample values.
5. Mark excluded sheets/tables with reasons: empty, metadata, duplicate summary, unrelated appendix, or outside scope.
6. For grouped tasks, report both raw-row count and reconstructed entity count.
7. Review unit guesses, time ranges, spatial fields, and key duplicate summaries before writing model assumptions.

## Blockers

Treat these as blockers for final numeric conclusions:

- Required file/sheet not inspected.
- Time range or row count contradicts the problem statement.
- Key field is missing or has unresolved duplicates.
- Unit conversion is unclear for headline results.
- Excluded table may contain required data.
