# Solve Prompt Expansions

Use this file when the user asks to solve one subquestion, solve a full problem,
finish a question, or “帮我做”.

## Completed Prompt: Solve One Subquestion

Trigger examples:

- 帮我求解第一问
- 只做第 2 问
- 完成 Q3
- 第四问怎么做

Internally expand to:

1. Identify the requested subquestion and inspect the problem statement,
   relevant attachments, existing `problem/`, `data/`, `modeling/`, `src/`,
   `tables/`, `figures/`, `results/`, and `paper/main.tex`.
2. Parse the subquestion: input, output, decision/model object, constraints,
   units, time/space scope, data dependencies, and hidden scoring points.
3. Create or update `modeling/qx_modeling_idea.md` before solving. It must
   include:
   - this question's role in the whole problem;
   - assumptions, variables, parameters, units, constraints, and boundaries;
   - baseline route, primary route, and fallback route;
   - beginner-readable derivation from problem wording to equations/criteria;
   - validation, sensitivity, feasibility, error, or boundary-case plan;
   - figure plan and paper-writing plan.
4. Add a detailed **代码建模流程** section in `modeling/qx_modeling_idea.md`.
   Explain:
   - which raw files or sheets are read;
   - how fields are renamed, filtered, merged, sorted, grouped, or converted;
   - how missing, abnormal, duplicate, or impossible records are handled;
   - how problem objects become code variables, arrays, matrices, sets, or
     solver inputs;
   - how each formula, objective, constraint, threshold, or state transition is
     implemented;
   - why each loop, search, simulation, optimizer, or solver call is needed;
   - what intermediate checks are saved before final results;
   - how solver status, infeasibility, boundary cases, and numerical failures
     are handled;
   - which output file contains each headline number;
   - which table or figure is intended for the paper;
   - how the code result is reverse-checked against the modeling idea.
5. Solve with reproducible code when calculation is needed. Save code, tables,
   figures, and validation notes under the standard folders.
6. Reverse-check code against the modeling idea. If the implementation differs,
   update the final modeling idea before writing the paper.
7. Update `results/validation_report.md` with headline number sources,
   validation evidence, solver status or feasibility checks, and limitations.
8. Write the current subquestion into `paper/main.tex` with deep prose:
   problem role, variables, assumptions, derivation, algorithm, result
   interpretation, validation, limitation, and handoff.
9. Run available checks before reporting completion.

Do not treat a single-question request as a smaller standard. It only narrows
scope; it does not remove derivation, reproducibility, validation, or paper text.

## Completed Prompt: Solve Full Problem

Trigger examples:

- 帮我做这道题
- 求解整题
- 完成这道数学建模题

Internally expand to:

1. Parse the full problem and all attachments.
2. Audit data files, sheets, fields, units, missing values, duplicates, time
   ranges, exclusions, and cross-question dependencies.
3. Build or update `problem/problem_parse.*`, `problem/task_plan.*`, and route
   comparison.
4. For each subquestion, follow the single-question completed prompt.
5. Connect subquestions through shared variables, assumptions, intermediate
   results, validation logic, and final conclusions.
6. Assemble `paper/main.tex` as one coherent paper, not a pile of fragments.
7. Write the abstract last from saved results and validation notes.
8. Apply first-prize-oriented checks for mechanism, validation, traceability,
   figure discipline, and paper readiness.
9. Run full validation checks before handoff.

## Full-Problem Guardrails

- Do not solve later questions by silently contradicting earlier assumptions.
- Do not let each question invent new symbols for the same object.
- Do not reuse a headline number unless its source file and meaning are clear.
- Do not use charts as a substitute for explaining why the model is correct.
- If time or data is insufficient, save the limitation and fallback route
  instead of pretending that a result is exact or optimal.
