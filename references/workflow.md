# CUMCM Workflow

Use this reference for full-problem solving, route design, and contest-time planning.

## 72-Hour Contest Workflow

| Time | Goal | Outputs |
| --- | --- | --- |
| 0-4 h | Read problem, audit attachments, decompose questions, choose route | task map, must-satisfy checklist, data inventory, 3-route comparison |
| 4-16 h | Q1 baseline model, data cleaning, first runnable code | baseline result, cleaned data, first tables/figures |
| 16-32 h | Q2/Q3 main model, optimization/prediction/evaluation solving | main scripts, result tables, preliminary validation |
| 32-44 h | Validation, sensitivity, robustness, figure finalization | error/feasibility/sensitivity tables, final figures |
| 44-60 h | TeX paper body, abstract, conclusion, appendix code | main `.tex`, captions, appendix run commands |
| 60-68 h | Judge-view review, consistency and traceability check | issue list, corrected numbers, result registry |
| 68-72 h | Final PDF, code/data/figure packaging | compiled PDF, source code, tables, figures, final checklist |

## Full Workflow

1. Parse the problem.
   - Split every subquestion into input -> decision/model object -> output -> validation.
   - Extract hard constraints, units, required attachments, and judging clues.
   - Build a must-satisfy checklist before solving.

2. Audit data when present.
   - Run the data profile script.
   - Inspect all Excel sheets and excluded tables.
   - Confirm covered time ranges, row counts, task reconstruction, and unit conversions.

3. Compare three routes.
   - Route A: baseline or analytical route.
   - Route B: main contest route.
   - Route C: robustness/fallback/extension route.
   - Select the route that maximizes correctness, validation, and paper clarity under time limits.

4. Build baseline before main computation.
   - Use simple formulas, bounds, greedy rules, naive forecasts, or small cases.
   - Use it to catch scale, direction, and feasibility errors.

5. Implement reproducibly.
   - Prefer deterministic Python unless the user requests MATLAB.
   - Save generated tables and figures with stable names.
   - Fix random seeds and report solver status when relevant.

6. Validate.
   - Match validation to task type: prediction error, optimization feasibility, ranking stability, simulation sensitivity, classification metrics, or boundary cases.
   - Mark missing validation as a limitation, not as success.

7. Write for judges.
   - Put the answer before method inventory.
   - Link every headline number to a table, figure, equation, output file, or assumption.
   - Keep only figures that support a conclusion.

## Final Deliverables

- Paper source and PDF when possible.
- Main code and run command.
- Data inventory and preprocessing notes.
- Result registry.
- Tables and figures with stable names.
- Figure captions and appendix code.
- Final score gate result.
