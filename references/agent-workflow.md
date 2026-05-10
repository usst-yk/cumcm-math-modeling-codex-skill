# Agent Workflow

This skill uses role cards as staged prompts inside Codex. It does not create a backend multi-agent system.

## Role Order

1. Problem Parser: extract subquestions, inputs, outputs, constraints, units, attachments, and risk words.
2. Coordinator: convert parse results into task plan and ambiguity points.
3. Data Auditor: inspect files, sheets, fields, missingness, units, time/spatial coverage, duplicates, and merge candidates.
4. Modeler: compare exactly three routes and create Qx model cards.
5. Solver: implement deterministic scripts and save outputs.
6. Validator: test feasibility, error, robustness, sensitivity, and artifact consistency.
7. Writer: write paper sections from registered results.
8. Reviewer: run final review and list blockers.

## Subquestion Loop

For full problems, process each Qx independently:

1. `problem/model_card_qx.md`
2. `src/qx_*.py`
3. `tables/tab_qx_*.csv|xlsx`
4. `figures/fig_qx_*.png|svg|pdf`
5. `results/result_registry.csv`
6. `results/validation_report.md`
7. `paper/sections/qx.tex`

Do not draft the final abstract until all solved subquestions have verified registry entries.

## Failure Policy

When a stage fails, do not hide the failure. Record it in `logs/error_log.md` or `results/validation_report.md`, simplify only when justified, and keep the limitation visible in the paper draft.
