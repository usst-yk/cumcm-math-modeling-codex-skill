# Stage Gates

Use these gates for full-problem solving and substantial single-question work.
If a gate fails, do not enter the next stage. Either return to the owner stage
and pass a recheck, or explicitly block/downgrade scope before proceeding.

For lightweight single-question work, apply the same checks mentally but do not
create empty templates or logs just to satisfy a gate. Save only the necessary
result files.

## Supervised Gate Output

For supervised, full-problem, or first-prize-level work, each gate should output
one of:

- `pass`: continue and record the evidence.
- `revise`: return to the named owner stage with a concrete fix and recheck
  evidence.
- `block`: stop or downgrade scope because a required fact, data file, result,
  or validation item is missing.

Use `agents/supervisor.md` for the decision. A supervisor finding must name:
owner, issue, expected fix, target rubric item, and evidence needed for recheck.
Use this schema for progress and notes:

- `gate_id`
- `decision`: `pass`, `revise`, or `block`
- `owner`
- `issue`
- `expected_fix`
- `target_rubric_item`
- `evidence_needed`
- `evidence`
- `rework_round`
- `attempt`

## Rework Loop Contract

For supervised, first-prize-level, or long-running projects, a gate is a closed
loop:

1. `gate_start`: record the current stage, owner, expected evidence, and attempt.
2. `revise` or `block`: record the failing rubric item, owner role, retry reason,
   and exact artifacts that must change.
3. `rework_done`: regenerate the relevant code, tables, figures, paper sections,
   or registry rows.
4. `recheck`: rerun the gate and record `done`, another `revise`, or explicit
   scope downgrade.

For these supervised modes, write each step to `logs/progress.jsonl` through
`scripts/update_progress.py`. Lean/default projects should record the same
failure and recheck facts in `results/validation_report.md` instead of creating
`logs/`. Required event fields for failed gates are `event_type`, `owner`,
`next_action`, `retry_reason`, and `evidence`. If a supervised progress
dashboard is being used and does not show the failure and recheck, the gate is
incomplete even if files were edited.

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
- the deliverable genre is set: `contest_paper`, `benchmark_report`,
  `route_review`, or `single_section`;
- assumptions and ambiguity points are separated from facts.

## Stage 1 -> Stage 2.5: Coordinator To Background Researcher

For full-problem, supervised, or first-prize-level work, do not finalize the
main route until:

- at least one official/nearby case, official commentary source, high-quality
  paper example, domain report, standard, or method reference has been checked
  when available;
- `problem/background_benchmark.md` exists or the benchmark search was recorded
  as unavailable with search scope and reason;
- transferable mechanisms, common failure modes, validation clues, and figure
  ideas are listed;
- unsafe borrowed ideas are marked as reference only, not copied as claims.
- for current or recent official contest problems, a cutoff date is recorded and
  post-problem writeups are excluded from model evidence.

For urgent single-question work, keep this as a short benchmark note instead of
creating a file.

## Stage 2 -> Stage 3: Data Auditor / Background Researcher To Modeler

Do not finalize routes until:

- all data files and Excel sheets are inventoried;
- excluded sheets/tables have written reasons;
- row counts, time ranges, and reconstructed entities are compared with the problem statement;
- missing values, duplicate keys, obvious outliers, and unit risks are recorded.
- the modeler has seen either the background benchmark or a written reason why
  no useful external benchmark is available;

## Stage 3 -> Stage 4: Modeler To Solver

Do not enter Solver until:

- exactly three routes have been compared;
- at least one baseline or simplified analytical route is defined;
- method trials are recorded when possible: baseline, primary, fallback,
  metric/result/failure, and the selected reason;
- every selected model has variables, objective/evaluation criterion, constraints, input data, output tables/figures, and validation plan;
- every selected model explains the derivation and solution procedure step by
  step, not only the final formulas;
- every selected route names benchmark evidence or an explicit gap, a target
  rubric item, a selling point, and the validation that would prove the selling
  point is not cosmetic;
- each Qx model card records a failure risk and where to return if validation
  fails: Modeler, Solver, Data Auditor, or Writer;
- a GPT-image model flowchart prompt path in `modeling/` or `modeling/flowcharts/` is
  planned, unless a written reason says a flowchart would be misleading;
- `modeling/qx_modeling_idea.md` / Qx model cards exist for the subquestions
  being solved.

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
  or `results/result_registry.csv`;
- run commands are stated in the final answer or recorded in `logs/run_log.md`;
- solver status, random seed, or failure status is recorded when relevant.
- baseline-vs-main comparison, small-case hand check, boundary check, or
  constraint violation check exists for any headline improvement claim.

## Stage 5 -> Stage 6: Validator To Writer

Do not write final paper text until:

- validation items are completed or explicitly marked unavailable with reasons;
- infeasible solver results, failed code, or missing data are not hidden;
- every figure/table has a source script or source data;
- the final modeling idea matches the code path, output tables, and generated
  figures;
- sensitivity analysis is based on actual perturbation or a reproducible perturbation plan.
- validation failures that overturn the conclusion are sent back to Modeler or
  Solver, not softened into prose.
- a scientific storyline exists for any `contest_paper`: research object,
  core contradiction, observed quantity, target quantity, model route,
  validation logic, and paper selling point.

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
- each solved Qx section makes its contribution visible in one restrained
  sentence and ties that contribution to a figure, table, or validation result;
- paper prose passes the anti-template writing rules in
  `references/paper-writing.md`.
- `contest_paper` main text does not expose skill, benchmark/test wording,
  registry status, raw script paths, CSV filenames, 回归测试, 本测试案例, or
  代码执行准确性.

## Stage 7 -> Stage 8: Paper Assembler To Abstract Writer

Do not write the final abstract until:

- the assembled paper body is coherent and no longer a collection of fragments;
- conclusion numbers and paper captions match the registry and generated
  artifacts;
- `scripts/validate_results.py --mode full` has no blocking paper-structure or
  traceability findings when project artifacts exist.
- `scripts/lint_paper_style.py --paper paper/main.tex --genre contest_paper`
  has no P1 findings before formal PDF delivery.

## Stage 8 -> Stage 9: Abstract Writer To Reviewer

Do not enter final review until:

- abstract numbers match `results/result_registry.csv`;
- table/figure captions match generated filenames;
- assumptions are used in the model or removed;
- paper references to figures/tables point to existing artifacts;
- appendix lists main script, inputs, outputs, dependencies, seed, and run command.
- AI-assisted figures, text, code, or references are declared according to
  `references/ai-compliance-reproducibility.md` when applicable;
- AI-generated schematic figures are clearly marked as schematic/conceptual and
  have passed human math/physics/data consistency review.

## Human-In-The-Loop

Ask once when route choices differ in objective definition, assumptions, or contest interpretation. If the user asks for full automation, choose the safest reproducible route and continue. If the difference is only implementation detail, proceed with the more reproducible option.
