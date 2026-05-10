# Stage Gates

Use these gates for full-problem solving and substantial single-question work. If a gate fails, either fix the blocker or record it in `logs/error_log.md` / `results/validation_report.md` before proceeding.

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
- Qx model cards exist for the subquestions being solved.

## Stage 4 -> Stage 5: Solver To Validator

Do not validate final conclusions until:

- code has produced saved output tables/figures;
- any useful schematic figure has been generated, or the reason for skipping it
  is stated in the final answer or recorded in `results/validation_report.md`;
- every headline value is traceable to a saved table, code output, problem fact,
  or `results/result_registry.csv`;
- run commands are stated in the final answer or recorded in `logs/run_log.md`;
- solver status, random seed, or failure status is recorded when relevant.

## Stage 5 -> Stage 6: Validator To Writer

Do not write final paper text until:

- validation items are completed or explicitly marked unavailable with reasons;
- infeasible solver results, failed code, or missing data are not hidden;
- every figure/table has a source script or source data;
- sensitivity analysis is based on actual perturbation or a reproducible perturbation plan.

## Stage 6 -> Stage 7: Writer To Reviewer

Do not enter final review until:

- abstract numbers match `results/result_registry.csv`;
- table/figure captions match generated filenames;
- assumptions are used in the model or removed;
- paper references to figures/tables point to existing artifacts;
- appendix lists main script, inputs, outputs, dependencies, seed, and run command.

## Human-In-The-Loop

Ask once when route choices differ in objective definition, assumptions, or contest interpretation. If the user asks for full automation, choose the safest reproducible route and continue. If the difference is only implementation detail, proceed with the more reproducible option.
