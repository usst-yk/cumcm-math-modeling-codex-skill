# Core Rules

Use this file for the persistent behavior that should not crowd `SKILL.md`.

## Core Behavior

- Correctness before speed: parse questions, constraints, units, outputs,
  attachments, and scoring clues first.
- Paper quality before speed: a complete TeX paper is better than a thin report.
- Full route design defaults to three routes: baseline, primary route, fallback.
- Urgent or single-question work may reduce empty files, but must not reduce
  problem analysis, route comparison, modeling depth, solving, validation, or
  paper writing.
- Before writing a full paper, follow:
  parse -> compare routes -> deepen model -> solve -> validate -> write body ->
  write abstract last.
- For major results, use `references/correctness-ladder.md`.
- Prefer transparent rigor over fashionable methods.

## Paper-First Loop

Process each subquestion as:

1. initial modeling idea;
2. code or analytical solve;
3. tables and figures;
4. code reverse-check against the idea;
5. final modeling idea;
6. result registry;
7. validation;
8. update `paper/main.tex`.

When the user asks to analyze, model, solve, validate, review, or write any part
of a CUMCM problem, update `paper/main.tex`. Do not interpret "solve Qx",
"求解第 x 问", or "完成第 x 问" as "only produce code/tables".

## Artifact Rules

- Inspect all sheets in every Excel workbook. State why any table is excluded.
- If sheets share a structure, concatenate them with a source-sheet column.
- Use stable lowercase names: `fig_q1_topic.png`, `tab_q1_topic.csv`.
- Create only supporting files needed for the current task, but always create
  or update `paper/main.tex`.
- Write `modeling/qx_modeling_idea.md` before solving. It must include the
  question role, task facts, assumptions, variables, step-by-step derivation,
  core equations or criterion, constraints, baseline, primary route, fallback
  route, algorithm, validation plan, figure plan, and paper-writing plan.
- After solving, compare the actual code path, equations, constraints, solver
  status, tables, and figures against `modeling/qx_modeling_idea.md`. If they
  differ, update the file before paper writing.
- Key numbers must trace to saved result tables, code output, problem facts, or
  `results/result_registry.csv`.
- All papers and paper drafts use TeX at `paper/main.tex`; Markdown is only for
  scratch notes or README-style explanation.
- Final papers must explain why the model is reasonable, how assumptions make
  the problem solvable, how variables/equations/constraints are built, why the
  algorithm is chosen, what each result means, and how validation supports it.
- Paper figures must use the bundled Chinese font assets by default so output
  looks consistent across macOS, Windows, and Linux.

## Hard Never Rules

- Never invent attachment fields, data values, references, rankings, distances,
  capacities, coordinates, optimal values, or error metrics.
- Never report optimality without solver status and feasibility checks.
- Never claim "模型精度较高" without an error metric or comparison baseline.
- Never write sensitivity analysis without actual perturbation or a reproducible
  perturbation plan.
- Never cite figures/tables that were not generated or provided.
- Never treat time pressure or single-question scope as a reason to reduce
  modeling depth, validation, figure coverage, or paper depth.
- Never leave "待补充" placeholders in final deliverables unless asked for a draft.
- Never push unrelated dirty files when syncing the skill to GitHub.
