# Final Review

Use this as a shorter alias for final judge-style review. For detailed scoring,
also read `references/final-checklist.md`. For claims about first-prize-level
quality, read `references/official-benchmark.md` and
`references/first-prize-rubric.md`.

## Required Checks

- Task coverage: every requested subquestion has a direct answer or a documented blocker.
- Data audit: all required files/sheets are inspected and exclusions are justified.
- saved tables, figures, code outputs, and validation notes: all headline numbers appear in `results/validation_report.md`.
- Validation: each task type has matching validation or a stated reason why validation is unavailable.
- Artifacts: referenced figures/tables exist and filenames match captions.
- Consistency: abstract, body, tables, figures, saved tables, figures, code outputs, and validation notes agree.
- Reproducibility: commands, main scripts, inputs, outputs, dependencies, and seeds are recorded.

Run `scripts/validate_results.py --project <project-dir>` when artifacts exist. Treat P1 findings as blockers.

## First-Prize-Level Claims

Do not say a route is first-prize level unless:

- it scores at least 16/20 in `references/first-prize-rubric.md`;
- no rubric item is 0;
- core mechanism, validation, and traceability each score 2;
- the nearest official benchmark source has been considered when available.
