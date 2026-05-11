# Stage Gates

Use these gates for full-problem solving and substantial single-question work. If a gate fails, either fix the blocker or record it in `results/validation_report.md` before proceeding.

For lightweight single-question work, apply the same checks mentally but do not
create empty templates or logs just to satisfy a gate. Save only the necessary
result files.

## Stage 0 -> Stage 1: Problem Parser To Coordinator

Do not build the task plan until:

- `problem/problem_parse.json` exists or parsing is explicitly impossible;
- subquestions, required outputs, constraints, units, time ranges, and attachment dependencies are extracted;
- risk words such as 全部, 至少, 不超过, 最优, 预测, 评价, 分别, 连续, 每个 are recorded.

## Stage 1 -> Stage 2: Coordinator To Data Auditor

Do not start modeling until:

- all subquestions are mapped to input -> model object -> output -> validation;
- hard constraints, units, time/spatial scale, and required attachments are listed;
- `problem/task_plan.json` exists or an equivalent task table has been written;
- assumptions and ambiguity points are separated from facts.

## Stage 2 -> Stage 3: Data Auditor To Modeler

Do not finalize routes until:

- all data files and Excel sheets are inventoried;
- excluded sheets/tables have written reasons;
- row counts, time ranges, and reconstructed entities are compared with the problem statement;
- missing values, duplicate keys, obvious outliers, and unit risks are recorded.

## Stage 3 -> Stage 4: Modeler To Solver

Do not enter Solver until:

- exactly three routes have been compared;
- at least one baseline or simplified analytical route is defined;
- every selected model has variables, objective/evaluation criterion, constraints, input data, output tables/figures, and validation plan;
- every selected model explains the derivation and solution procedure step by
  step, not only the final formulas;
- a GPT-image model flowchart prompt path in `modeling/` or `modeling/flowcharts/` is
  planned, unless a written reason says a flowchart would be misleading;
- `modeling/qx_modeling_idea.md` exists for the subquestions being solved.

## Stage 4 -> Stage 5: Solver To Validator

Do not validate final conclusions until:

- code has produced saved output tables/figures;
- code follows the model described in `modeling/qx_modeling_idea.md`, or the
  modeling idea has been updated to match the implemented model;
- `modeling/qx_modeling_idea.md` records the post-solve code reverse check;
- the figure plan has been executed: final model flowchart plus result figure
  for most solved questions, and validation/sensitivity figure when needed;
- if fewer than two figures are generated for a solved question, the reason is
  stated in the final answer or recorded in `results/validation_report.md`;
- every headline value is traceable to a saved table, code output, problem fact,
  or `results/validation_report.md`;
- run commands are stated in the final answer or recorded in `results/validation_report.md`;
- solver status, random seed, or failure status is recorded when relevant.

## Stage 5 -> Stage 6: Validator To Writer

Do not write final paper text until:

- validation items are completed or explicitly marked unavailable with reasons;
- infeasible solver results, failed code, or missing data are not hidden;
- every figure/table has a source script or source data;
- the final modeling idea matches the code path, output tables, and generated
  figures;
- sensitivity analysis is based on actual perturbation or a reproducible perturbation plan.

## Stage 6 -> Stage 7: Writer To Paper Assembler

Do not write the final abstract or enter final review until:

- solved subquestion content is written directly in `paper/main.tex`, not as
  separate `paper/sections/*.tex` fragments;
- `paper/main.tex` contains problem restatement, problem analysis, assumptions,
  notation, data audit/preprocessing, model establishment and solution,
  validation/sensitivity analysis, model evaluation, conclusion, and appendix
  or clear equivalents;
- each solved subquestion part explains mechanism, mathematics, algorithm, result, and
  validation, not only numbers and figures;
- later questions explicitly state how they reuse earlier assumptions,
  variables, parameters, results, or strategy outputs.
- `paper/main.tex` explains the code-verified final modeling idea, not an
  obsolete pre-code plan.

## Stage 7 -> Stage 8: Paper Assembler To Abstract Writer

Do not write the final abstract until:

- the assembled paper body is coherent and no longer a collection of fragments;
- conclusion numbers and paper captions match the saved tables, figures, code outputs, and validation notes and generated
  artifacts;
- `scripts/validate_results.py --mode full` has no blocking paper-structure or
  traceability findings when project artifacts exist.

## Stage 8 -> Stage 9: Abstract Writer To Reviewer

Do not enter final review until:

- abstract numbers match `results/validation_report.md`;
- table/figure captions match generated filenames;
- assumptions are used in the model or removed;
- paper references to figures/tables point to existing artifacts;
- appendix lists main script, inputs, outputs, dependencies, seed, and run command.

## Human-In-The-Loop

Ask once when route choices differ in objective definition, assumptions, or contest interpretation. If the user asks for full automation, choose the safest reproducible route and continue. If the difference is only implementation detail, proceed with the more reproducible option.
