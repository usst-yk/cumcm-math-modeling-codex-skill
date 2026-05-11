# CUMCM Workflow

Use this reference for full-problem solving, route design, and contest-time planning.

For beginner-facing solving, keep supporting files purposeful, but always
maintain `paper/main.tex`. Read `references/output-policy.md` before creating
template files. Avoiding empty templates must not reduce figures, analysis,
modeling, validation, or paper writing.

## 72-Hour Contest Workflow

| Time | Goal | Outputs |
| --- | --- | --- |
| 0-4 h | Read problem, audit attachments, decompose questions, choose route | task map, must-satisfy checklist, data inventory, 3-route comparison |
| 4-16 h | Q1 baseline model, data cleaning, first runnable code | baseline result, cleaned data, first tables/figures |
| 16-32 h | Q2/Q3 main model, optimization/prediction/evaluation solving | main scripts, result tables, preliminary validation |
| 32-44 h | Validation, sensitivity, robustness, figure finalization | error/feasibility/sensitivity tables, final figures |
| 44-60 h | TeX paper body, conclusion, appendix code | main `.tex`, captions, appendix run commands |
| 60-64 h | Final abstract after subquestion results, figures, and validation are stable | traceable abstract draft |
| 64-68 h | Judge-view review, consistency and traceability check | issue list, corrected numbers, result registry |
| 68-72 h | Final PDF, code/data/figure packaging | compiled PDF, source code, tables, figures, final checklist |

## Full Workflow

1. Problem Parser: parse the official statement.
   - Split subquestions and extract required outputs, constraints, units, time ranges, attachments, and risk words.
   - Write `problem/problem_parse.json` and `problem/problem_parse.md` before modeling.

2. Coordinator: build the task plan.
   - Split every subquestion into input -> decision/model object -> output -> validation.
   - Extract hard constraints, units, required attachments, and judging clues.
   - Build `problem/task_plan.json`, `problem/task_plan.md`, and a must-satisfy checklist before solving.

3. Data Auditor: audit data when present.
   - Run the data profile script.
   - Inspect all Excel sheets and excluded tables.
   - Confirm covered time ranges, row counts, task reconstruction, and unit conversions.

4. Modeler: compare three routes.
   - Route A: baseline or analytical route.
   - Route B: main contest route.
   - Route C: robustness/fallback/extension route.
   - Select the route that maximizes correctness, validation, and paper clarity under time limits.

5. Solver: solve subquestions one by one.
   - For each Qx, first write `modeling/qx_modeling_idea.md`, then implement
     code and save only the needed result table and figures.
   - After running code, compare the actual implementation with the modeling
     idea. Update `modeling/qx_modeling_idea.md` with the final code-verified
     modeling idea, then write it directly into `paper/main.tex`.
   - Before coding each Qx, make a figure plan using `references/figure-plan.md`.
     Default to a model schematic plus a result figure.
   - Use detailed modeling ideas and result registry for every solved question
     whose numbers enter the paper. Use separate run logs mainly for full
     projects; this affects logging only, not modeling, validation, or paper
     writing.
   - Do not draft the final abstract before solved subquestions have traceable
     result tables or registered results.

6. Build baseline before main computation.
   - Use simple formulas, bounds, greedy rules, naive forecasts, or small cases.
   - Use it to catch scale, direction, and feasibility errors.

7. Implement reproducibly.
   - Prefer deterministic Python unless the user requests MATLAB.
   - Save generated tables and figures with stable names.
   - Generate Chinese model schematics, result figures, and validation figures
     according to the figure plan.
   - Fix random seeds and report solver status when relevant.

8. Validator: validate.
   - Match validation to task type: prediction error, optimization feasibility, ranking stability, simulation sensitivity, classification metrics, or boundary cases.
   - Check whether code, result tables, figures, and the modeling idea describe
     the same model.
   - Mark missing validation as a limitation, not as success.

9. Writer: write judge-facing subquestion content directly in `paper/main.tex`.
   - Put the answer before method inventory.
   - Link every headline number to a table, figure, equation, output file, or assumption.
   - Write the final code-verified modeling idea, including any important
     difference from the initial idea.
   - Keep only figures that support a conclusion.

10. Abstract Writer: write the final abstract last.
   - Use `agents/abstract_writer.md`.
   - Summarize every solved subquestion with method, headline result, and
     validation evidence.
   - Check abstract numbers against body, tables, figures, conclusion, and
     result registry.

11. Reviewer: review before handoff.
   - Run final artifact checks before handoff.

## Final Deliverables

Standard single-question handoff:

- Main answer and limitation.
- Current-question modeling idea.
- Current-question code when code was needed.
- One result table.
- Usually two Chinese figures: model schematic and result figure.
- Validation/sensitivity figure when needed.
- `results/result_registry.csv` for headline values used in the paper.
- `paper/main.tex`.

The handoff is paper-first and paper-complete: do not shorten analysis,
formulas, solution reasoning, validation explanation, or paper writing.

Full-project handoff:

- Paper source and PDF when possible.
- Main code and run command.
- Data inventory and preprocessing notes.
- Result registry.
- Tables and figures with stable names.
- Figure captions and appendix code.
- Final score gate result.
