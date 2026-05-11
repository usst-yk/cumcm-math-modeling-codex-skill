# Agent Workflow

This skill uses role cards as staged prompts inside Codex. It does not create a backend multi-agent system.

## Role Order

1. Problem Parser: extract subquestions, inputs, outputs, constraints, units, attachments, and risk words.
2. Coordinator: convert parse results into task plan and ambiguity points.
3. Data Auditor: inspect files, sheets, fields, missingness, units, time/spatial coverage, duplicates, and merge candidates.
4. Modeler: compare exactly three routes and create Qx modeling idea files.
5. Solver: implement deterministic scripts from the modeling idea and save outputs.
6. Validator: test feasibility, error, robustness, sensitivity, and code-to-model consistency.
7. Writer: write `paper/main.tex` from registered results.
8. Abstract Writer: write the final abstract after solved subquestions and results are stable.
9. Reviewer: run final review and list blockers.

## Subquestion Loop

For full problems, process each Qx independently. In beginner-facing file-lean
mode, create only the files that are actually needed for the current question.
This file policy must not reduce problem analysis, route comparison, modeling,
solving, validation, or paper writing.

File-lean Qx loop:

1. `modeling/qx_modeling_idea.md`.
2. `src/solve_qx.py` when code is needed.
3. `tables/tab_qx_result.csv|xlsx`.
4. `figures/fig_qx_model_schematic.png|svg`.
5. `figures/fig_qx_result.png|svg`.
6. `figures/fig_qx_validation.png|svg` when a check is needed.
7. `paper/main.tex` only when paper text is requested.

After code runs, update `modeling/qx_modeling_idea.md` with the code reverse
check. The final paper must use the code-verified modeling idea, not the
pre-solve draft if they differ.

Full project Qx loop:

1. `modeling/qx_modeling_idea.md`
2. `src/qx_*.py`
3. `tables/tab_qx_*.csv|xlsx`
4. `figures/fig_qx_*.png|svg|pdf`
5. `results/result_registry.csv`
6. `results/validation_report.md`
7. `paper/main.tex`

Full projects must also keep `modeling/qx_modeling_idea.md` consistent with
the executed code before paper writing.

Do not draft the final abstract until solved subquestions have traceable result
tables or verified registry entries. Keep all paper text in `paper/main.tex`.
When writing the abstract, use
`agents/abstract_writer.md`.

## Failure Policy

When a stage fails, do not hide the failure. Record it in `logs/error_log.md` or `results/validation_report.md`, simplify only when justified, and keep the limitation visible in the paper draft.
