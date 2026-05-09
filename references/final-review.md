# Final Review

Use this as a shorter alias for final judge-style review. For detailed scoring, also read `references/final-checklist.md`.

## Required Checks

- Task coverage: every requested subquestion has a direct answer or a documented blocker.
- Data audit: all required files/sheets are inspected and exclusions are justified.
- Registry: all headline numbers appear in `results/result_registry.csv`.
- Validation: each task type has matching validation or a stated reason why validation is unavailable.
- Artifacts: referenced figures/tables exist and filenames match captions.
- Consistency: abstract, body, tables, figures, appendix, and registry agree.
- Reproducibility: commands, main scripts, inputs, outputs, dependencies, and seeds are recorded.

Run `scripts/validate_results.py --project <project-dir>` when artifacts exist. Treat P1 findings as blockers.
