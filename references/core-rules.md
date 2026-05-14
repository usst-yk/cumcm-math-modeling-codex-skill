# Core Rules

Use this file for the persistent behavior that should not crowd `SKILL.md`.

## 目录

- Core Behavior
- Paper-First Loop
- Artifact Rules
- Hard Never Rules

## Core Behavior

- Correctness before speed: parse questions, constraints, units, outputs,
  attachments, and scoring clues first.
- Paper quality before speed: a complete TeX paper is better than a thin report.
- Award-oriented rule: the judged product is the paper, not code, scratch notes,
  or chat. A strong model only raises the ceiling; `paper/main.tex` must make
  solved models, results, validation, and conclusions visible, coherent, and
  checkable to judges.
- First-prize default: every CUMCM task follows
  `references/first-prize-workflow.md`. Official benchmark comparison and the
  critical gates for core mechanism, validation, traceability, and paper
  readiness are default checks, not optional extras.
- Full route design defaults to three routes: baseline, primary route, fallback.
- Urgent or single-question work may reduce empty files, but must not reduce
  problem analysis, route comparison, modeling depth, solving, validation, or
  paper writing.
- Before writing a full paper, follow:
  parse -> compare routes -> deepen model -> solve -> validate -> write body ->
  write abstract last.
- For major results, use `references/correctness-ladder.md`.
- Prefer transparent rigor over fashionable methods.
- Do not describe a CUMCM deliverable as complete, award-ready, or
  first-prize-level while any critical gate is missing.

## Paper-First Loop

Process each subquestion as:

1. initial modeling idea;
2. code or analytical solve;
3. tables and figures;
4. code reverse-check against the idea;
5. final modeling idea;
6. saved tables, figures, code outputs, and validation notes;
7. validation;
8. update `paper/main.tex`.

For every solved subquestion, prepare paper-ready material immediately:

- the role of this subquestion in the whole paper;
- variables, assumptions, objective/evaluation function, constraints, and
  outputs;
- result tables, Chinese figures, captions, and explanatory prose;
- baseline, error, feasibility, sensitivity, robustness, or boundary checks;
- variables, parameters, assumptions, metrics, or intermediate results shared
  with later subquestions.

When the user asks to solve, write, revise, or turn code/results into a paper,
update `paper/main.tex`. When validation or review changes a paper-facing claim,
update the paper too. Planning-only tasks such as problem parsing, route
comparison, candidate model brainstorming, or pre-solve derivation may stop at
`problem/`, `modeling/`, or `results/`, but must state what would later enter
the paper. Do not interpret "solve Qx", "求解第 x 问", or "完成第 x 问" as
"only produce code/tables".

## Artifact Rules

- Inspect all sheets in every Excel workbook. State why any table is excluded.
- If sheets share a structure, concatenate them with a source-sheet column.
- Use stable lowercase names: `fig_q1_topic.png`, `tab_q1_topic.csv`.
- Create only supporting files needed for the current task. Create or update
  `paper/main.tex` when the task is solved, paper-facing, or changes a paper
  claim; otherwise keep planning artifacts ready for later paper writing.
- Write `modeling/qx_modeling_idea.md` before solving. It must include the
  question role, task facts, assumptions, variables, step-by-step derivation,
  core equations or criterion, constraints, baseline, primary route, fallback
  route, detailed code modeling process, algorithm, validation plan, figure
  plan, and paper-writing plan.
- The step-by-step derivation must follow
  `references/modeling-derivation-standard.md`: translate problem wording into
  variables, mechanism, equations/criteria, constraints, algorithm, validation
  hooks, and paper wording. A formula list without prose derivation is
  incomplete.
- After solving, compare the actual code path, equations, constraints, solver
  status, tables, and figures against `modeling/qx_modeling_idea.md`. If they
  differ, update the file before paper writing.
- The code modeling process must be written in `modeling/qx_modeling_idea.md`,
  not only implied by scripts. It should map problem data to code variables,
  explain preprocessing, show how each equation or rule is implemented, describe
  loops/search/solver calls, list intermediate sanity checks, and name the saved
  tables, figures, and validation records.
- Key numbers must trace to saved result tables, code output, problem facts, or
  `results/validation_report.md`.
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
- Never rely on brute-force enumeration as the final "model" unless the search
  space is small enough to enumerate exactly and the paper explains why that
  enumeration is complete. For larger contest problems, use assumptions,
  structure, decomposition, optimization, simulation, or bounds to make the
  problem sufficiently realistic, solvable, and verifiable.
- Never cite figures/tables that were not generated or provided.
- Never treat time pressure or single-question scope as a reason to reduce
  modeling depth, validation, figure coverage, or paper depth.
- Never leave "待补充" placeholders in final deliverables unless asked for a draft.
- Never push unrelated dirty files when syncing the skill to GitHub.
