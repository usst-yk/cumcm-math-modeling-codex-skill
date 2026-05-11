# Result Tracking

Use this reference whenever `paper/main.tex`, abstract, conclusion, or policy recommendation contains numbers.

## Registry Rule

For full projects and final paper delivery, any numerical conclusion in the
abstract, conclusion, result section, captions, or final recommendations must
appear in `results/result_registry.csv`.

For file-lean single-question work, a formal registry is optional. This only
relaxes the registry file requirement; the number still must trace to a saved
result table, code output, or problem fact.

Do not write final headline numbers directly from memory, chat text, or an
unsaved terminal output. Save the source table/log first; register the value
when a full project registry exists or final paper delivery is requested.

## Required Columns

`templates/result_registry.csv` uses:

```csv
id,subquestion,claim,value,unit,source_type,source_file,source_line_or_cell,script,command,figure_or_table,validation,status,created_at,verified_by,notes
```

Recommended status values:

- `draft`: value is extracted but not fully checked.
- `verified`: source file exists and validation is complete.
- `blocked`: value cannot be trusted because code/data/validation failed.

## Claim Types

Register:

- optimal objective values and selected decisions;
- prediction metrics and forecast headline values;
- ranking results and top/bottom entities;
- simulation peaks, thresholds, and final states;
- sensitivity-analysis conclusions;
- values quoted in abstract or conclusion.

## Writer Rule

Before writing final paper text:

1. Read the registry.
2. Use only `verified` rows for final claims.
3. If a required claim is `draft`, label the relevant part of `paper/main.tex` as draft.
4. If a required claim is `blocked`, write the blocker instead of a conclusion.
